from drivers.state_lookup import *
from drivers.deserializer import *
from drivers.calibration_processor import *
from agent import *
import numpy as np
import matplotlib.pyplot as plt
import argparse

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

    NEUTRAL_OF_ACCEL_X = -50
    NEUTRAL_OF_ACCEL_Y = 8290
    NEUTRAL_OF_ACCEL_Z = 810

    SENSOR_MIN_OF_ACCEL_X = -8200
    SENSOR_MIN_OF_ACCEL_Y = -8200
    SENSOR_MIN_OF_ACCEL_Z = -8200

    SENSOR_MAX_OF_ACCEL_X = 8200
    SENSOR_MAX_OF_ACCEL_Y = 8200
    SENSOR_MAX_OF_ACCEL_Z = 8200

    serial_port = configure_and_open(PORT)
    agent = Agent()

    while True:
        sensor_data = get_all_sensor_data(serial_port)
        scaled_accel = Accelerometer()
        scaled_accel.x = scale_sensors(100, sensor_data.accel.x, SENSOR_MAX_OF_ACCEL_X, SENSOR_MIN_OF_ACCEL_X, NEUTRAL_OF_ACCEL_X)
        scaled_accel.y = scale_sensors(100, sensor_data.accel.y, SENSOR_MAX_OF_ACCEL_Y, SENSOR_MIN_OF_ACCEL_Y, NEUTRAL_OF_ACCEL_Y)
        scaled_accel.z = scale_sensors(100, sensor_data.accel.z, SENSOR_MAX_OF_ACCEL_Z, SENSOR_MIN_OF_ACCEL_Z, NEUTRAL_OF_ACCEL_Z)
        print("scaled accel x " + str(scaled_accel.x))
        print("scaled accel y " + str(scaled_accel.y))
        print("scaled accel z " + str(scaled_accel.z))
        state = get_state_based_on_accel(scaled_accel)
        print(state)
        agent.perform_action(state.lower())


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
