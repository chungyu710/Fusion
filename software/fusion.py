from drivers.state_lookup import *
from drivers.deserializer import *
from drivers.calibration_processor import *
from agent import *
import numpy as np
import matplotlib.pyplot as plt


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

    serial_port = configure_and_open(PORT)
    agent = Agent()
    i = 0
    for i in range(2000000000):
        sensor_data = get_all_sensor_data(serial_port)
        print(sensor_data.accel_data)
        plt.axis([0, 500, -10000, 10000])

        plt.scatter(i, sensor_data.accel_data.y)
        plt.pause(0.01)

    plt.show()
        # i+= 1
        # scaled_accel = Accelerometer(0,0,0)
        # scaled_accel.x = scale_sensors(100, sensor_data.accel_data.x, SENSOR_MAX_OF_ACCEL_X, SENSOR_MIN_OF_ACCEL_X, NEUTRAL_OF_ACCEL_X)
        # scaled_accel.y = scale_sensors(100, sensor_data.accel_data.y, SENSOR_MAX_OF_ACCEL_Y, SENSOR_MIN_OF_ACCEL_Y, NEUTRAL_OF_ACCEL_Y)
        # scaled_accel.z = scale_sensors(100, sensor_data.accel_data.z, SENSOR_MAX_OF_ACCEL_Z, SENSOR_MIN_OF_ACCEL_Z, NEUTRAL_OF_ACCEL_Z)
        # state = get_state_based_on_accel(scaled_accel)
        # agent.perform_action(state.lower())


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
