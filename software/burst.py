import argparse

from drivers import deserializer
from time import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)
    args = parser.parse_args()

    ser = deserializer.open(args.port)
    deserializer.configure(ser)

    while True:
        #start_time = time()
        deserializer.burst(ser)
        #end_time = time()
        #print(f"latency: {end_time - start_time}")