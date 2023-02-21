import argparse
import log

from drivers import deserializer
from drivers.common import *
from time import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', required=True)
    args = parser.parse_args()

    set_log_level("success")
    deserializer.open(args.port, sync = False)

    while True:
        deserializer.dump()
