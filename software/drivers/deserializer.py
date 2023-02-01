from drivers.common import *
from drivers.protocol import *

import serial
import log
import struct
import time

BAUDRATE = 115200

# This indicates how many times we want to retry before resetting the device
MAX_RETRIES = 5

def configure_and_open(port):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=BAUDRATE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            bytesize=serial.EIGHTBITS
        )
    except Exception as e:
        log.error("Error opening serial port: ", e)
        exit(ERROR)

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    retries = 0
    # TODO (Shusil) : Maybe use exponential backoff
    while (True):
        if retries > MAX_RETRIES:
            log.info(f"Tried more than: {MAX_RETRIES} times, resetting the device")
            reset(ser)
        if not ping(ser):
            log.warning(f"Glove not responding!!! attempt: {retries}")
            retries += 1
        else:
            break

    return ser

def send_command(ser, command):
    # Little endian byte
    ser.write(struct.pack("<B", command))

def verify_checksum(header, payload):
    checksum = header.status ^ header.size
    payload = bytes(payload)

    for i in range(header.size):
        checksum ^= payload[i]

    if checksum != header.checksum:
        log.error("Checksum mismatch")
        print(str(header))
        return False

    return True

def ping(ser):
    log.info("PING")
    send_command(ser, COMMAND_PING)
    header = get_header_data(ser)

    # TODO: Uncomment it after ping command functionality uploaded to the device
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        return False

    return True

def reset(ser):
    log.info("RESET")
    send_command(ser, COMMAND_RESET)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

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
    send_command(ser, COMMAND_SENSORS)
    header = get_header_data(ser)
    payload = ser.read(header.size)   # Get the payload "size" bytes

    if not verify_checksum(header, payload):
        reset(ser)
        exit(ERROR)
    if header.status != STATUS_SUCCESS:
        log.error(f"Status: {header.status}")
        exit(ERROR)

    return parse_sensor_data(payload)

def stream_start(ser):
    command = COMMAND_STREAM | STREAM_START
    send_command(ser, command)
    header = get_header_data(ser)

    #if not verify_checksum(header, []):
    #    exit(ERROR)
    #if header.status != STATUS_SUCCESS:
    #    log.error(f"Status: {header.status}")
    #    exit(ERROR)

def stream_stop(ser):
    command = COMMAND_STREAM | STREAM_STOP
    send_command(ser, command)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    #send_command(ser, COMMAND_PING)
    #header = get_header_data(ser)

    #if not verify_checksum(header, []):
    #    exit(ERROR)
    #if header.status != STATUS_SUCCESS:
    #    log.error(f"Status: {header.status}")
    #    exit(ERROR)
