import argparse
import time
import log

from drivers import deserializer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)
    args = parser.parse_args()

    deserializer.open(args.port)
    deserializer.configure()
    deserializer.start()
    log.suppress(log.Level.DEBUG)

    while True:
        start_time = time.time()

        deserializer.pop()

        end_time = time.time()
        latency = (end_time - start_time) * 1000
        print("latency: %.2f ms" % (latency))
