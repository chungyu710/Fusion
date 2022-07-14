from socket import timeout
from parso import parse
from requests import head
from drivers.common import *
import argparse
import serial
import argparse
import time
import log

BAUDRATE = 115200
HEADER_SIZE = 3 # bytes
STATUS_SUCCESS         = 0,
STATUS_ERROR           = 1,
STATUS_UNKNOWN_REQUEST = 2,
STATUS_LOW_BATTERY     = 3

REQUEST_ALL_SENSORS = b"\x30"
REQUEST_ACCEL = b"\x31"
REQUEST_GYRO = b"\x32"
REQUEST_FLEX = b"x33"

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
        print("Error opening serial port: ", e)
        exit(0)

    retries = 0
    # TODO (Shusil) : Maybe use exponential backoff
    while (True):
        if retries > MAX_RETRIES:
            print("Tried more than: " + MAX_RETRIES + " times", "resetting the device")
            # TODO: Send RESET command (not implemented on firmware yet)
        if not ping(ser):
            print("Glove not responding!!! attempt:", retries)
            retries += 1
            time.sleep(0.2)
        else:
            break

    return ser

def ping(ser):
    send(PING, ser)
    status, length, checksum = get_header_data(ser)
    
    # TODO: Uncomment it after ping command functionality uploaded to the device
    # if status != STATUS_SUCCESS:
    #     return False
    
    return True

def send(msg, ser):
    ser.write(msg)

def create_object(command, payload):
    #TODO: Revisit and remove hardcodes
    if command == REQUEST_ALL_SENSORS:
        i = 0
        accel_x, accel_y, accel_z = int.from_bytes(payload[i:i+2], "little", signed=True), int.from_bytes(payload[i+2:i+4], "little", signed=True), int.from_bytes(payload[i+4:i+6], "little", signed=True)
        accel_data = Accelerometer(accel_x, accel_y, accel_z)
        log.debug("Accelerometer data: " + str(accel_data))
        i += 6

        gyro_pitch, gyro_yaw, gyro_roll = int.from_bytes(payload[i:i+2], "little", signed=True), int.from_bytes(payload[i+2:i+4], "little", signed=True), int.from_bytes(payload[i+4:i+6], "little", signed=True)
        gyro_data = Gyro(gyro_pitch, gyro_yaw, gyro_roll)
        log.debug("Gyro data: " + str(gyro_data))
        i += 6

        flex_thumb, flex_index, flex_middle, flex_ring, flex_pinky = int.from_bytes(payload[i:i+2], "little", signed=True), int.from_bytes(payload[i+2:i+4], "little", signed=True), int.from_bytes(payload[i+4:i+6], "little", signed=True), int.from_bytes(payload[i+6:i+8], "little", signed=True), int.from_bytes(payload[i+8:i+10], "little", signed=True)
        flex_data = Flex(flex_thumb, flex_index, flex_middle, flex_ring, flex_pinky)
        log.debug("Flex data: " + str(flex_data))

        sensor = Sensors(accel_data, gyro_data, flex_data)
        log.info("sensor data: \n" + str(sensor))

        return sensor
    
    else:
        # TODO: Add more commands here
        log.note("COMMAND NOT SUPPORTED ATM!")


def get_header_data(ser):
    # Get the response header, should be HEADER_SIZE bytes
    header_data = ser.read(HEADER_SIZE)
    log.debug("header_data: " + str(header_data))
    
    status, length, checksum = header_data[0], header_data[1], header_data[2]
    log.debug("status: " + str(status))
    log.debug("length: " + str(length))
    log.debug("checksum: " + str(checksum))

    return status, length, checksum

def get_all_sensor_data(ser):
    command = REQUEST_ALL_SENSORS
    send(command, ser)

    status, length, checksum = get_header_data(ser)

    # TODO: Add logic for status and checksum
    log.info(f"status: {status}")

    # Get the payload of size "length"
    payload = ser.read(length)

    # print(payload)
    return create_object(command, payload)
