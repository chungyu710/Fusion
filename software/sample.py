import argparse
from drivers.calibration_processor import *
from drivers.deserializer import *
from time import time, sleep
from threading import Thread
import pyautogui

fifo = []

def move_mouse():
    while True:
        if len(fifo) > 0:
            sensors = fifo.pop()
            #print(sensors)
            sensors.gyro.pitch = scale_sensors(50, sensors.gyro.pitch, 4000, -4000, 46)
            sensors.gyro.roll = scale_sensors(50, sensors.gyro.roll, 4000, -4000, 22)
            sensors.gyro.yaw = scale_sensors(50, sensors.gyro.yaw, 4000, -4000, -42)
            pyautogui.move(sensors.gyro.yaw, sensors.gyro.pitch)
        else:
            print("waiting")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)

    args = parser.parse_args()

    serial_port = configure_and_open(args.port)
    log.disable()
    t = Thread(target=move_mouse)
    t.start()

    while True:
        start_time = time()
        n = 1
        responses = get_all_sensor_data(serial_port)
        end_time = time()
        fifo.append(responses)
        print(f"latency: {end_time - start_time}")
        #for i in range(n):
        #    print(responses[i])




