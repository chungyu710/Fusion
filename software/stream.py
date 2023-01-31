import argparse

from drivers.deserializer import *
from time import time, sleep

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', required = True)
    parser.add_argument('--port', required=True)

    args = parser.parse_args()

    serial_port = configure_and_open(args.port)

    start_time = time()

    start = int(args.start)

    if (start == 1):
        log.info("START STREAM")
        start_streaming(serial_port)
    else:
        log.info("STOP STREAM")
        stop_streaming(serial_port)

    end_time = time()
    print(f"latency: {end_time - start_time}")
    #print(sensors)
