from socket import timeout
from parso import parse
from common import *
import argparse
import serial
import logging
import argparse

BAUDRATE = 115200

def configure_and_open():
    ser = serial.Serial(
        port=PORT,
        baudrate=BAUDRATE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1,
        bytesize=serial.EIGHTBITS
    )

    try:
        ser.open()
    except Exception as e:
        print("Error opening serial port: ", e)
        exit(0)

    # TODO (Shusil) : Use exponential backoff
    while (true):
        if not ping(ser):
            print("Glove not responding!!!")
    return ser

def ping(ser):
    send(PING, ser)

def send(msg, ser):
    ser.write(msg)

def get_all_sensor_data():
    ser = configure_and_open()
    command = bin(3)
    send(command, ser)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)

    args = parser.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler("debug.log", 'w'), logging.StreamHandler()])

    get_all_sensor_data()
    