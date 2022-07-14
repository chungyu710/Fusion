from socket import timeout
from parso import parse
from requests import head
from common import *
import argparse
import serial
import logging
import argparse
import time

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

def configure_and_open():
    try:
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUDRATE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            bytesize=serial.EIGHTBITS
        )
    except Exception as e:
        print("Error opening serial port: ", e)
        exit(0)

    # while True:
    #     time.sleep(1)
    #     print(ser.read(10))

    # TODO (Shusil) : Use exponential backoff
    # while (True):
    #     if not ping(ser):
    #         print("Glove not responding!!!")

    return ser

def ping(ser):
    send(PING, ser)

def send(msg, ser):
    ser.write(msg)

def create_object(command, payload):
    #TODO: Revisit and remove hardcodes
    if command == REQUEST_ALL_SENSORS:
        i = 0
        accel_x, accel_y, accel_z = int.from_bytes(payload[i:i+2], "little", signed=True), int.from_bytes(payload[i+2:i+4], "little", signed=True), int.from_bytes(payload[i+4:i+6], "little", signed=True)
        accel_data = Accelerometer(accel_x, accel_y, accel_z)
        logging.debug("Accelerometer data: " + str(accel_data))
        i += 6

        gyro_pitch, gyro_yaw, gyro_roll = int.from_bytes(payload[i:i+2], "little", signed=True), int.from_bytes(payload[i+2:i+4], "little", signed=True), int.from_bytes(payload[i+4:i+6], "little", signed=True)
        gyro_data = Gyro(gyro_pitch, gyro_yaw, gyro_roll)
        logging.debug("Gyro data: " + str(gyro_data))
        i += 6

        flex_thumb, flex_index, flex_middle, flex_ring, flex_pinky = int.from_bytes(payload[i:i+2], "little", signed=True), int.from_bytes(payload[i+2:i+4], "little", signed=True), int.from_bytes(payload[i+4:i+6], "little", signed=True), int.from_bytes(payload[i+6:i+8], "little", signed=True), int.from_bytes(payload[i+8:i+10], "little", signed=True)
        flex_data = Flex(flex_thumb, flex_index, flex_middle, flex_ring, flex_pinky)
        logging.debug("Flex data: " + str(flex_data))

        sensor = Sensors(accel_data, gyro_data, flex_data)
        logging.info("sensor data: \n" + str(sensor))

        return sensor
    
    else:
        # TODO: Add more commands here
        logging.info("COMMAND NOT SUPPORTED ATM!")


def get_all_sensor_data():
    ser = configure_and_open()
    command = REQUEST_ALL_SENSORS
    send(command, ser)

    # Get the response header, should be HEADER_SIZE bytes
    header_data = ser.read(HEADER_SIZE)
    logging.debug("header_data: " + str(header_data))
    
    status, length, checksum = header_data[0], header_data[1], header_data[2]
    logging.debug("status: " + str(status))
    logging.debug("length: " + str(length))
    logging.debug("checksum: " + str(checksum))

    # TODO: Add logic for status and checksum

    # Get the payload of size "length"
    payload = ser.read(length)

    # print(payload)
    return create_object(command, payload)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)

    args = parser.parse_args()
    PORT = args.port

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler("debug.log", 'w'), logging.StreamHandler()])

    while True:
        sensor_data = get_all_sensor_data()