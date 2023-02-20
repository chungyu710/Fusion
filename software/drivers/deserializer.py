from drivers.common import *
from drivers.protocol import *
from threading import Thread

import serial
import log
import struct
import time
import signal

BAUDRATE = 115200
TIMEOUT_S = 1

queue = []   # RX queue of Sensor objects
ser = None

# This indicates how many times we want to retry before resetting the device
MAX_TRIES = 5

def open(port):
    global ser
    try:
        ser = serial.Serial(
            port=port,
            baudrate=BAUDRATE,
            stopbits=serial.STOPBITS_ONE,
            timeout=TIMEOUT_S,
            bytesize=serial.EIGHTBITS
        )
    except Exception as e:
        log.error(f"Error opening serial port: {e}")
        abort()

    purge()
    log.success(f"Opened serial port '{port}'")

def close():
    purge()
    ser.close()
    log.success("Closed serial port")

def purge():
    log.info("Purge serial port")
    ser.reset_input_buffer()
    ser.reset_output_buffer()

def configure():
    pings = 0
    resets = 0
    while not ping():
        log.info("Pinging Fusion...")
        pings += 1
        purge()
        if pings > MAX_TRIES:
            log.warning(f"Fusion did not respond after {MAX_TRIES} pings")
            log.info(f"Resetting MCU")
            send(COMMAND_RESET)
            resets += 1
            purge()
            time.sleep(2)   # give the MCU time to restart the firmware
            if resets > MAX_TRIES:
                log.error(f"Failed to reset glove after {MAX_TRIES} tries")
                abort()

            pings = 0   # go back to pinging

def send(command):
    # Little endian byte
    ser.write(struct.pack("<B", command))
    ser.flush()
    ser.flushOutput()

def verify_checksum(header, payload):
    checksum = header.status ^ header.size
    payload = bytes(payload)

    if payload is None or len(payload) != header.size:
        log.error("Incorrect payload size")
        return False

    for i in range(header.size):
        checksum ^= payload[i]

    if checksum != header.checksum:
        log.error("Checksum mismatch")
        print(str(header))
        return False

    return True

def ping():
    log.info("PING")
    send(COMMAND_PING)
    header = get_header_data()

    if header is None:
        return False
    if not verify_checksum(header, []):
        return False
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        return False

    return True

def reset():
    log.info("RESET")
    send(COMMAND_RESET)
    #purge()
    header = get_header_data()

    if header is None:
        return False
    if not verify_checksum(header, []):
        return False
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        return False

    return True

def parse_sensor_data(payload):
    sensors = Sensors()
    sensors.unpack(payload)
    log.debug("------- SENSORS -------\r\n" + str(sensors))
    return sensors

def get_header_data():
    # Get the response header, should be Header.SIZE bytes
    header = Header()
    data = ser.read(Header.SIZE)

    if len(data) != Header.SIZE:
        log.error("Failed to read header data bytes")
        abort()

    header.unpack(data)

    #log.debug("------- HEADER -------\r\n" + str(header))
    return header

def get_all_sensor_data():
    log.debug("SAMPLE")
    send(COMMAND_SAMPLE)
    header = get_header_data()
    payload = ser.read(header.size)

    if not verify_checksum(header, payload):
        abort()
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        abort()

    return parse_sensor_data(payload)

def burst():
    log.debug("BURST")
    send(COMMAND_BURST)

    for i in range(10):
        start_time = time.time()

        header = get_header_data()
        payload = ser.read(header.size)

        end_time = time.time()
        latency = (end_time - start_time) * 1000
        print("latency: %.2f ms" % (latency))

        if not verify_checksum(header, payload):
            abort()
        if header.status != STATUS_SUCCESS:
            log.error(f"Status: {header.status}")
            abort()

        parse_sensor_data(payload)

#def stream_start(ser):
#    command = COMMAND_STREAM | STREAM_START
#    send(ser, command)
#    header = get_header_data(ser)

#    if header is None:
#        abort()
#    if not verify_checksum(header, []):
#        abort()
#    if header.status != STATUS_SUCCESS:
#        log.error(f"Status: {header.status}")
#        abort()

#def stream_stop(ser):
#    command = COMMAND_STREAM | STREAM_STOP
#    send(ser, command)
#    #ser.reset_input_buffer()
#    #ser.reset_output_buffer()

#    #send(ser, COMMAND_PING)
#    #header = get_header_data(ser)

#    #if not verify_checksum(header, []):
#    #    abort()
#    #if header.status != STATUS_SUCCESS:
#    #    log.error(f"Status: {header.status}")
#    #    abort()

def pop():
    if len(queue) > 0:
        return queue.pop(0)
    else:
        log.debug("SAMPLE")
        send(COMMAND_SAMPLE)
        #log.warning("No sensor data available")
        return None

def rx_thread():
    while rx_thread_enable:
        header = get_header_data()
        payload = ser.read(header.size)

        if not verify_checksum(header, payload):
            abort()

        if header.status != STATUS_SUCCESS:
            log.error(f"Status: {header.status}")
            abort()

        sensors = parse_sensor_data(payload)
        queue.append(sensors)

    log.success("Ended RX thread")

def abort():
    global rx_thread_enable
    rx_thread_enable = False
    thread.join()
    close()

def ctrl_c_handler(signum, frame):
    abort()

def start():
    global rx_thread_enable
    rx_thread_enable = True
    thread.start()

rx_thread_enable = False
thread = Thread(target = rx_thread)
signal.signal(signal.SIGINT, ctrl_c_handler)
