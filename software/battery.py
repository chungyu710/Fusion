import argparse
import log

from drivers import deserializer
from drivers.common import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='info')
    parser.add_argument('--port', required=True)
    args = parser.parse_args()

    set_log_level(args.log_level)
    deserializer.open(args.port)

    while True:
        battery = deserializer.battery()
        print(battery)
