from drivers.common import *
from drivers.protocol import *

import serial
import log
import struct
import time

BAUDRATE = 115200
TIMEOUT_S = 1

# This indicates how many times we want to retry before resetting the device
MAX_TRIES = 5

def open(port):
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
        exit(ERROR)

    purge(ser)
    return ser

def close(ser):
    purge(ser)
    ser.close()

def purge(ser):
    log.info("Purge serial port")
    ser.reset_input_buffer()
    ser.reset_output_buffer()

def configure(ser):
    pings = 0
    resets = 0
    while not ping(ser):
        log.info("Pinging Fusion...")
        pings += 1
        purge(ser)
        if pings > MAX_TRIES:
            log.warning(f"Fusion did not respond after {MAX_TRIES} pings")
            log.info(f"Resetting MCU")
            send(ser, COMMAND_RESET)
            resets += 1
            purge(ser)
            time.sleep(2)   # give the MCU time to restart the firmware
            if resets > MAX_TRIES:
                log.error(f"Failed to reset glove after {MAX_TRIES} tries")
                exit(ERROR)
            pings = 0   # go back to pinging

def send(ser, command):
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
        print(str(header))
        return False

    return True

def ping(ser):
    log.info("PING")
    send(ser, COMMAND_PING)
    header = get_header_data(ser)

    if not verify_checksum(header, []):
        return False
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        return False

    return True

def reset(ser):
    log.info("RESET")
    send(ser, COMMAND_RESET)
    purge(ser)
    header = get_header_data(ser)

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

def get_header_data(ser):
    # Get the response header, should be Header.SIZE bytes
    data = ser.read(Header.SIZE)
    fields = struct.unpack("<BBB", data)   # little endian

    header = Header()
    header.status = fields[0]
    header.size = fields[1]
    header.checksum = fields[2]

    log.debug("------- HEADER -------\r\n" + str(header))
    return header

def get_all_sensor_data(ser):
    log.debug("SENSORS")
    send(ser, COMMAND_SAMPLE)
    header = get_header_data(ser)
    payload = ser.read(header.size)

    if not verify_checksum(header, payload):
        exit(ERROR)
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        exit(ERROR)

    return parse_sensor_data(payload)

def stream_start(ser):
    command = COMMAND_STREAM | STREAM_START
    send(ser, command)
    header = get_header_data(ser)

    if not verify_checksum(header, []):
        exit(ERROR)
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        exit(ERROR)

def stream_stop(ser):
    command = COMMAND_STREAM | STREAM_STOP
    send(ser, command)
    #ser.reset_input_buffer()
    #ser.reset_output_buffer()

    #send(ser, COMMAND_PING)
    #header = get_header_data(ser)

    #if not verify_checksum(header, []):
    #    exit(ERROR)
    #if header.status != STATUS_SUCCESS:
    #    log.error(f"Status: {header.status}")
    #    exit(ERROR)
