import argparse
from operator import iadd

from drivers.deserializer import *
from time import time, sleep

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)

    args = parser.parse_args()

    serial_port = configure_and_open(args.port)
    #log.disable()

    #print("Resetting...")
    #send(b"\x50", serial_port)
    #sleep(1)

    #while True:
    #    send(b"\x40", serial_port)
    #    status, length, checksum = get_header_data(serial_port)
    #    log.info(f"status: {status}")
    #    payload = serial_port.read(length)
    #    print(parse_unsigned(payload))

    while True:
        start_time = time()
        sensors = get_all_sensor_data(serial_port)
        end_time = time()
        print(f"latency: {end_time - start_time}")
        print(sensors)
