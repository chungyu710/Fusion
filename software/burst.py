import argparse
import log

from drivers import deserializer
from time import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)
    args = parser.parse_args()

    deserializer.open(args.port)

    while True:
        begin = time()
        sensors = deserializer.burst()
        end = time()
        latency = (end - begin) * 1000
        log.info("Latency: %.3f ms" % (latency))
