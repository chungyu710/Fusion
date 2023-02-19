from drivers.common import *
from drivers.protocol import *

import serial
import log
import struct

BAUDRATE = 115200
STATUS_SUCCESS         = 0,
STATUS_ERROR           = 1,
STATUS_UNKNOWN_REQUEST = 2,
STATUS_LOW_BATTERY     = 3

REQUEST_ALL_SENSORS = b"\x30"
REQUEST_ACCEL = b"\x31"
REQUEST_GYRO = b"\x32"
REQUEST_FLEX = b"\x33"
STREAM_START = b"\x60"
STREAM_STOP = b"\x61"
PING = b"\x00"

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
        exit(-1)

    retries = 0
    # TODO (Shusil) : Maybe use exponential backoff
    while (True):
        if retries > MAX_RETRIES:
            log.error("Tried more than: " + MAX_RETRIES + " times", "resetting the device")
            # TODO: Send RESET command (not implemented on firmware yet)
        if not ping(ser):
            log.warning("Glove not responding!!! attempt:", retries)
            retries += 1
        else:
            break

    return ser

def ping(ser):
    send(PING, ser)
    header = get_header_data(ser)

    # TODO: Uncomment it after ping command functionality uploaded to the device
    # if status != STATUS_SUCCESS:
    #     return False

    return True

def send(msg, ser):
    ser.write(msg)

def parse_signed(bytes):
    return int.from_bytes(bytes, 'little', signed=True)

def parse_unsigned(bytes):
    return int.from_bytes(bytes, 'little', signed=False)

def create_object(command, payload):
    #TODO: Revisit and remove hardcodes
    if command == REQUEST_ALL_SENSORS:
        i = 0
        accel = Accelerometer()
        accel.x = parse_signed(payload[i:i+2])
        accel.y = parse_signed(payload[i+2:i+4])
        accel.z = parse_signed(payload[i+4:i+6])
        i += 6

        gyro = Gyro()
        gyro.pitch = parse_signed(payload[i:i+2])
        gyro.roll = parse_signed(payload[i+2:i+4])
        gyro.yaw = parse_signed(payload[i+4:i+6])
        i += 6

        flex = Flex()
        flex.thumb = parse_unsigned(payload[i:i+2])
        flex.index = parse_unsigned(payload[i+2:i+4])
        flex.middle = parse_unsigned(payload[i+4:i+6])
        flex.ring = parse_unsigned(payload[i+6:i+8])
        flex.pinky = parse_unsigned(payload[i+8:i+10])
        i += 10

        print("payload", payload)
        button = Button()
        button.pressed = payload[i]

        sensors = Sensors(accel, gyro, flex, button)
        log.debug("------- SENSORS -------\r\n" + str(sensors))

        return sensors

    else:
        # TODO: Add more commands here
        log.note("COMMAND NOT SUPPORTED ATM!")


def get_header_data(ser):
    # Get the response header, should be RESPONSE_HEADER_SIZE bytes
    header = ser.read(RESPONSE_HEADER_SIZE)
    fields = struct.unpack("BBB", header)

    response = Response()
    response.status = fields[0]
    response.length = fields[1]
    response.checksum = fields[2]

    log.debug("------- HEADER -------\r\n" + str(response))
    return response

def get_all_sensor_data(ser):
    command = REQUEST_ALL_SENSORS
    send(command, ser)
    header = get_header_data(ser)

    # TODO: Add logic for status and checksum

    # Get the payload of size "length"
    payload = ser.read(header.length)

    # print(payload)
    return create_object(command, payload)

def start_streaming(ser):
    command = STREAM_START
    send(command, ser)
    header = get_header_data(ser)
    # TODO: Add logic for status and checksum
    log.info(f"status: {header.status}")

def stop_streaming(ser):
    command = STREAM_STOP
    send(command, ser)
    header = get_header_data(ser)
    # TODO: Add logic for status and checksum
    log.info(f"status: {header.status}")
