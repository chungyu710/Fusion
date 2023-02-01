import argparse

from drivers.deserializer import *
from time import time, sleep

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', required = True)
    parser.add_argument('--port', required=True)
    args = parser.parse_args()
    start = int(args.start)

    port = configure_and_open(args.port)
    begin = time()

    if (start == 1):
        log.info("START STREAM")
        stream_start(port)
    else:
        log.info("STOP STREAM")
        stream_stop(port)

    end = time()
    print(f"latency: {end - begin}")
