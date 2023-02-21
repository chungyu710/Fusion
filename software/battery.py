import argparse
import log

from drivers import deserializer
from drivers.common import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='info')
    parser.add_argument('--hand', required=True, choices = ["left", "right"])
    parser.add_argument('--mode', required=True, choices = ["wired", "wireless"])

    args = parser.parse_args()
    HAND = args.hand
    MODE = args.mode

    set_log_level(args.log_level)
    port = deserializer.get_serial_port(HAND, MODE)
    deserializer.open(port)

    while True:
        battery = deserializer.battery()
        print(battery)
