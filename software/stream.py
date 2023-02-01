import argparse

from drivers.deserializer import *
from time import time, sleep

import pyautogui

pyautogui.PAUSE = 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', required = True)
    parser.add_argument('--port', required=True)
    args = parser.parse_args()
    start = int(args.start)

    ser = configure_and_open(args.port)

    if (start == 1):
        log.info("START STREAM")
        stream_start(ser)
        min = 1923834
        max = 0
        total = 0
        count = 0
        while True:
            begin = time()
            sensors = get_all_sensor_data(ser)
            end = time()

            latency = end - begin

            if latency > max:
                max = latency
            if latency < min:
                min = latency

            count += 1
            total += latency
            avg = total / count

            print(f"latency: {latency * 1000} ms, min: {min * 1000} ms, max: {max * 1000} ms, avg: {avg * 1000} ms")
            pyautogui.move(sensors.gyro.pitch, 0)
    else:
        log.info("STOP STREAM")
        stream_stop(ser)
