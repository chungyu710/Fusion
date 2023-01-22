from drivers.state_lookup import *
from drivers.deserializer import *
from drivers.calibration_processor import *
from time import time, sleep
from agent import *
import argparse

pyautogui.PAUSE = 0   # reduces pyautogui lag

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

    SENSOR_MIN_OF_FLEX = 529
    SENSOR_MAX_OF_FLEX = 816

    NEUTRAL_OF_FLEX = 676
    NEUTRAL_OF_PITCH = 46
    NEUTRAL_OF_ROLL = 22
    NEUTRAL_OF_YAW = -42

    MOUSE_MODE = "00000"
    CLICK_MODE = "01000"
    RIGHT_CLICK_MODE = "01100"
    DOUBLE_CLICK_MODE = "10000"
    SWIPE_MODE = "01110"
    SCROLL_MODE = "11000"
    RECENTER = "11111"

    serial_port = configure_and_open(PORT)
    agent = Agent()
    previousState = None
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
        
        sensors.flex.thumb = scale_sensors(50, sensors.flex.thumb, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)        
        sensors.flex.index = scale_sensors(50, sensors.flex.index, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)        
        sensors.flex.middle = scale_sensors(50, sensors.flex.middle, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)        
        sensors.flex.ring = scale_sensors(50, sensors.flex.ring, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)        
        sensors.flex.pinky = scale_sensors(50, sensors.flex.pinky, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)

        state = get_stated_based_on_flex(sensors.flex)
        state = state.lower()
        log.debug("State: " + str(state))

        if (state in [MOUSE_MODE, CLICK_MODE, RIGHT_CLICK_MODE]):  
            if(state == CLICK_MODE):
                if previousState != CLICK_MODE: 
                    pyautogui.mouseDown()
            elif (state == RIGHT_CLICK_MODE):
                pyautogui.mouseDown(button='right')
            else:
                print("about to do mouse up hfiafiuhiduasfidhshfsdfuisdiufisudfhsiudfhsdfhsdi")
                pyautogui.mouseUp()
                pyautogui.mouseUp(button='right')
                          
            pyautogui.move(sensors.gyro.yaw, sensors.gyro.pitch)

        elif state == DOUBLE_CLICK_MODE: 
            if(not previousState == DOUBLE_CLICK_MODE):
                # pyautogui.doubleClick()
                pass

        elif state == SCROLL_MODE:
            if sensors.gyro.pitch > 0:
                pyautogui.scroll(1)
            elif sensors.gyro.pitch < 0:
                pyautogui.scroll(-1)
                
        elif state == RECENTER:
            pyautogui.moveTo(maxWidth // 2, maxHeight // 2)
            
        else:
            log.debug("not in a recognizable state")

        previousState = state
        print(sensors)
        #agent.perform_action(state.lower())
