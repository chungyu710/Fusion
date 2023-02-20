from drivers.common import *
from drivers.protocol import *

import serial
import log
import struct
import time
import signal

BAUDRATE = 115200   # UART baud rate
TIMEOUT_S = 1       # serial port timeout in seconds
RESET_DELAY_S = 2   # time to wait after issuing a reset so that MCU firmware can reboot
MAX_TRIES = 5       # maximum times the glove is reset before giving up on the handshake

ser = None    # serial port
pending = 0   # number of pending sensor packets (burst mode only)

def ctrl_c_handler(signum, frame):
    print()
    abort(SUCCESS)

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
        abort(ERROR)

    signal.signal(signal.SIGINT, ctrl_c_handler)
    purge()
    log.success(f"Opened serial port '{port}'")
    handshake()

def close():
    purge()
    ser.close()
    log.success("Closed serial port")

def purge():
    ser.reset_input_buffer()
    ser.reset_output_buffer()

def abort(result):
    close()
    exit(result)

def handshake():
    tries = 0
    while not ping():
        tries += 1
        if tries > MAX_TRIES:
            log.error(f"Glove did not respond after {MAX_TRIES} tries")
            abort(ERROR)

        reset()

    log.success(f"Established communication with glove")

def send(command):
    # little endian (<)
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
    purge()
    time.sleep(RESET_DELAY_S)   # give the MCU time to restart the firmware

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
        abort(ERROR)

    header.unpack(data)
    log.debug("------- HEADER -------\r\n" + str(header))
    return header

def sample():
    log.info("SAMPLE")
    send(COMMAND_SAMPLE)
    header = get_header_data()
    payload = ser.read(header.size)

    if not verify_checksum(header, payload):
        abort(ERROR)

    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        abort(ERROR)

    return parse_sensor_data(payload)

def burst():
    global pending
    if pending < BURST_SIZE:
        log.info(f"Requesting {BURST_SIZE} sensor samples")
        log.info("BURST")
        send(COMMAND_BURST)
        pending += BURST_SIZE

    header = get_header_data()
    payload = ser.read(header.size)

    if not verify_checksum(header, payload):
        abort(ERROR)

    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        abort(ERROR)

    pending -= 1
    log.success("Received sensor data")
    return parse_sensor_data(payload)
