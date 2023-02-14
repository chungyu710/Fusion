from drivers.state_lookup import *
from drivers.deserializer import *
from drivers.calibration_processor import *
from time import time, sleep
from agent import *
import argparse

pyautogui.PAUSE = 0   # reduces pyautogui lag
pyautogui.FAILSAFE = False # take out pyautogui failsafe

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='DEBUG')
    parser.add_argument('--port', required=True)

    args = parser.parse_args()
    PORT = args.port

    NEUTRAL_OF_ACCEL_X = -200
    NEUTRAL_OF_ACCEL_Y = 8290
    NEUTRAL_OF_ACCEL_Z = 1162

    SENSOR_MIN_OF_ACCEL_X = -8200
    SENSOR_MIN_OF_ACCEL_Y = -8200
    SENSOR_MIN_OF_ACCEL_Z = -8200

    SENSOR_MAX_OF_ACCEL_X = 8200
    SENSOR_MAX_OF_ACCEL_Y = 8200
    SENSOR_MAX_OF_ACCEL_Z = 8200

    SENSOR_MAX_OF_GYRO = 4000
    SENSOR_MIN_OF_GYRO = -4000

    SENSOR_MIN_OF_FLEX_THUMB = 529
    SENSOR_MIN_OF_FLEX_INDEX = 529
    SENSOR_MIN_OF_FLEX_MIDDLE = 529
    SENSOR_MIN_OF_FLEX_RING = 816
    SENSOR_MIN_OF_FLEX_PINKY = 816

    SENSOR_MAX_OF_FLEX_THUMB = 529
    SENSOR_MAX_OF_FLEX_INDEX = 529
    SENSOR_MAX_OF_FLEX_MIDDLE = 529
    SENSOR_MAX_OF_FLEX_RING = 816
    SENSOR_MAX_OF_FLEX_PINKY = 816
    

    NEUTRAL_OF_FLEX = 676
    NEUTRAL_OF_PITCH = 46
    NEUTRAL_OF_ROLL = 22
    NEUTRAL_OF_YAW = -42

    MOUSE_MODE = "00000"
    CLICK_MODE = "01000" #holding mouse down
    RIGHT_CLICK_MODE = "11000"
    SINGLE_CLICK_MODE = "00001" # single click
    SWIPE_MODE = "01110" #not implemented 
    SCROLL_MODE = "01100"
    RECENTER = "11111" # not used for now

    serial_port = configure_and_open(PORT)
    agent = Agent()
    prev_state = "00000"
    maxWidth, maxHeight = pyautogui.size()

    while True:
        sensors = get_all_sensor_data(serial_port)

        sensors.gyro.pitch = scale_sensors(100, sensors.gyro.pitch, SENSOR_MAX_OF_GYRO, SENSOR_MIN_OF_GYRO, NEUTRAL_OF_PITCH)
        sensors.gyro.roll = scale_sensors(100, sensors.gyro.roll, SENSOR_MAX_OF_GYRO, SENSOR_MIN_OF_GYRO, NEUTRAL_OF_ROLL)
        sensors.gyro.yaw = scale_sensors(100, sensors.gyro.yaw, SENSOR_MAX_OF_GYRO, SENSOR_MIN_OF_GYRO, NEUTRAL_OF_YAW)

        if(sensors.gyro.yaw > -3 and sensors.gyro.yaw < 3):
            sensors.gyro.yaw = 0
        if(sensors.gyro.pitch > -3 and sensors.gyro.pitch < 3):
            sensors.gyro.pitch = 0
        
        #sensors.flex.thumb = scale_sensors(50, sensors.flex.thumb, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)        
        #sensors.flex.index = scale_sensors(50, sensors.flex.index, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)        
        #sensors.flex.middle = scale_sensors(50, sensors.flex.middle, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)        
        #sensors.flex.ring = scale_sensors(50, sensors.flex.ring, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)        
        #sensors.flex.pinky = scale_sensors(50, sensors.flex.pinky, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)

        # state = get_stated_based_on_flex(sensors.flex)
        state = get_flex_state(sensors.flex, prev_state)

        if sensors.button.pressed:
            state = RECENTER

        log.debug("State: " + str(state))
        # log.debug("sensors: " + str(sensors))

        if (state in [MOUSE_MODE, CLICK_MODE, RIGHT_CLICK_MODE]):  
            if(state == CLICK_MODE):
                if prev_state != CLICK_MODE: 
                    pyautogui.mouseDown()
            elif (state == RIGHT_CLICK_MODE):
                pyautogui.mouseDown(button='right')
            else:
                pyautogui.mouseUp()
                pyautogui.mouseUp(button='right')
                          
            pyautogui.move(-sensors.gyro.yaw, -sensors.gyro.pitch)

        elif state == SINGLE_CLICK_MODE: 
            if(prev_state != SINGLE_CLICK_MODE):
                pyautogui.click()

        elif state == SCROLL_MODE:
            if sensors.gyro.pitch > 0:
                pyautogui.scroll(1)
            elif sensors.gyro.pitch < 0:
                pyautogui.scroll(-1)

        elif state == RECENTER:
            pyautogui.moveTo(maxWidth // 2, maxHeight // 2)

        else:
            log.debug("not in a recognizable state")

        prev_state = state
        print(sensors)
        #agent.perform_action(state.lower())
