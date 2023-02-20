from drivers.common import *
from drivers.protocol import *
from multiprocessing import Process

import serial
import log
import struct
import time
import signal

BAUDRATE = 115200
TIMEOUT_S = 1

queue = []   # RX queue of Sensor objects
ser = None
pending = 0

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

    log.success(f"Opened serial port '{port}'")
    purge()

def close():
    purge()
    ser.close()
    log.success("Closed serial port")

def purge():
    ser.reset_input_buffer()
    ser.reset_output_buffer()

def configure():
    #pings = 0
    #resets = 0

    #while not ping():
    #    log.info("Pinging glove")
    #    pings += 1
    #    purge()

    #    if pings > MAX_TRIES:
    #        log.warning(f"Glove did not respond after {MAX_TRIES} pings")
    #        log.info(f"Resetting MCU")
    #        send(COMMAND_RESET)
    #        resets += 1

    #        if resets > MAX_TRIES:
    #            log.error(f"Failed to reset glove after {MAX_TRIES} tries")
    #            abort()

    #        purge()
    #        time.sleep(2)   # give the MCU time to restart the firmware
    #        pings = 0   # go back to pinging

    tries = 0
    while not ping():
        tries += 1
        if tries > MAX_TRIES:
            log.warning(f"Glove did not respond after {MAX_TRIES} tries")
            abort()

        log.info("RESET")
        send(COMMAND_RESET)
        purge()
        time.sleep(2)   # give the MCU time to restart the firmware

def send(command):
    # Little endian byte
    ser.write(struct.pack("<B", command))
    ser.flush()

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

    log.success("Ping response received")
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

    log.debug("------- HEADER -------\r\n" + str(header))
    return header

def get_all_sensor_data():
    log.info("SAMPLE")
    send(COMMAND_SAMPLE)
    header = get_header_data()
    payload = ser.read(header.size)

    if not verify_checksum(header, payload):
        abort()
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        abort()

    return parse_sensor_data(payload)

def rx_stream():
    header = get_header_data()
    payload = ser.read(header.size)

    if not verify_checksum(header, payload):
        abort()
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        abort()

    return parse_sensor_data(payload)

def burst():
    global pending
    log.info("BURST")
    send(COMMAND_BURST)
    pending += BURST_SIZE

def service():
    global pending
    if pending < BURST_SIZE:
        log.info(f"Requesting {BURST_SIZE} sensor samples")
        burst()

    header = get_header_data()
    payload = ser.read(header.size)

    if not verify_checksum(header, payload):
        abort()
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        abort()

    pending -= 1
    log.success("Received sensor data")
    return parse_sensor_data(payload)

#signal.signal(signal.SIGINT, ctrl_c_handler)

def abort():
    #global rx_thread_enable
    #rx_thread_enable = False
    #thread.join()
    #process.kill()
    close()
    exit(ERROR)

def ctrl_c_handler(signum, frame):
    abort()

def stream_start():
    send(COMMAND_STREAM | STREAM_START)

def stream_stop():
    send(COMMAND_STREAM | STREAM_STOP)
