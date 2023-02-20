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
    #deserializer.start()
    #log.suppress(log.Level.DEBUG)

    while True:
        sensors = deserializer.service()
        pass
