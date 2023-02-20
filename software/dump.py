import argparse
import log

from drivers import deserializer
from time import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)
    args = parser.parse_args()

    deserializer.open(args.port, sync = False)

    while True:
        deserializer.dump()
