from tabnanny import verbose
from drivers.state_lookup import *
from drivers.deserializer import *
from drivers.calibration_processor import *
from agent import *
import numpy as np
import matplotlib.pyplot as plt
import argparse
from drivers.velocity import *

pyautogui.PAUSE = 0   # reduces pyautogui lag

#import logging

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='INFO')
    parser.add_argument('--port', required=True)

    args = parser.parse_args()
    PORT = args.port

    #logging.basicConfig(level=args.log_level,
    #                    format="%(asctime)s [%(levelname)s] %(message)s",
    #                    handlers=[logging.FileHandler("debug.log", 'w'), logging.StreamHandler()])

    NEUTRAL_OF_ACCEL_X = -200
    NEUTRAL_OF_ACCEL_Y = 8290
    NEUTRAL_OF_ACCEL_Z = 1162

    SENSOR_MIN_OF_ACCEL_X = -8200
    SENSOR_MIN_OF_ACCEL_Y = -8200
    SENSOR_MIN_OF_ACCEL_Z = -8200

    SENSOR_MAX_OF_ACCEL_X = 8200
    SENSOR_MAX_OF_ACCEL_Y = 8200
    SENSOR_MAX_OF_ACCEL_Z = 8200

    serial_port = configure_and_open(PORT)
    agent = Agent()

    while True:
        sensors = get_all_sensor_data(serial_port)
        sensors.accel.x = scale_sensors(100, sensors.accel.x, SENSOR_MAX_OF_ACCEL_X, SENSOR_MIN_OF_ACCEL_X, NEUTRAL_OF_ACCEL_X)
        sensors.accel.y = scale_sensors(100, sensors.accel.y, SENSOR_MAX_OF_ACCEL_Y, SENSOR_MIN_OF_ACCEL_Y, NEUTRAL_OF_ACCEL_Y)
        sensors.accel.z = scale_sensors(100, sensors.accel.z, SENSOR_MAX_OF_ACCEL_Z, SENSOR_MIN_OF_ACCEL_Z, NEUTRAL_OF_ACCEL_Z)
        print(sensors.accel)

        state = get_state_based_on_accel(sensors.accel)
        print(state)

        velocity = calculate_velocity(sensors.accel)
        print(velocity)

        #pyautogui.move(abs(sensors.accel.z), 0)

        sensors.gyro.roll = scale_sensors(50, sensors.gyro.roll, 4000, -4000, 21)
        sensors.gyro.yaw = scale_sensors(50, sensors.gyro.yaw, 4000, -4000, -37)
        print(sensors.gyro)
        pyautogui.move(-sensors.gyro.roll, -sensors.gyro.yaw)
        #agent.perform_action(state.lower())


# code from agent
# agent = Agent()
# try:
#     while True:
#         # TODO: pass in acceleration array
#         state = state_lookup.get_state_based_on_accel("pass in acceleration array here")
#         agent.perform_action(state.lower())
# except KeyboardInterrupt:
#     print('\n')

# neutral
# x min: -80
# x max: -30

# y min: -540
# y max: -520

# z min: 8310
# z max: 8330

# up
# x min:
