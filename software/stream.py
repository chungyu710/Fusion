import argparse
import log

from drivers import deserializer
from time import time, sleep

import pyautogui

pyautogui.PAUSE = 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', required = True)
    parser.add_argument('--port', required=True)
    args = parser.parse_args()
    start = int(args.start)

    ser = deserializer.open(args.port)
    deserializer.configure(ser)

    if (start == 1):
        log.info("START STREAM")
        deserializer.stream_start(ser)
        #min = 1923834
        #max = 0
        #total = 0
        #count = 0
        while True:
            begin = time()
            sensors = deserializer.get_all_sensor_data(ser)
            end = time()

            latency = end - begin
            log.debug(latency)

            #if latency > max:
            #    max = latency
            #if latency < min:
            #    min = latency

            #count += 1
            #total += latency
            #avg = total / count

            #print(f"latency: {latency * 1000} ms, min: {min * 1000} ms, max: {max * 1000} ms, avg: {avg * 1000} ms")
            #pyautogui.move(sensors.gyro.pitch, 0)
    else:
        log.info("STOP STREAM")
        deserializer.stream_stop(ser)

    deserializer.close(ser)
