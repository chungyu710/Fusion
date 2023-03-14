from drivers.state_lookup import *
from drivers import deserializer
from drivers.calibration_processor import *
from time import time, sleep
from agent import *
from drivers.common import *

import argparse

pyautogui.PAUSE = 1e-6   # reduces pyautogui lag
pyautogui.FAILSAFE = False # take out pyautogui failsafe

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', default='info')
    parser.add_argument('--port', required=True)
    parser.add_argument('--latency', required=False, action = "store_true")

    args = parser.parse_args()
    PORT = args.port
    LOG_LEVEL = args.log_level
    LATENCY = args.latency
    set_log_level(LOG_LEVEL)

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

    SCALE_RANGE = 50

    MOUSE_MODE = "00000"
    CLICK_MODE = "01000" #holding mouse down
    RIGHT_CLICK_MODE = "11000"
    SINGLE_CLICK_MODE = "00001" # single click
    SWIPE_MODE = "01110" #not implemented
    SCROLL_MODE = "01100"
    RECENTER = "11111" # not used for now

    DEADZONE = 2

    agent = Agent()
    prev_state = "00000"
    maxWidth, maxHeight = pyautogui.size()

    deserializer.open(PORT)
    samples = [0 for i in range(10)]

    log.info("Starting state machine")

    while True:
        if LATENCY:
            begin = time()

        sensors = deserializer.burst()

        if LATENCY:
            end = time()
            latency = (end - begin) * 1000
            samples.append(latency)
            samples.pop(0)

            average = 0
            for s in samples:
                average += s
            average /= len(samples)

            log.info("latency: %.3f ms (average: %.3f ms)" % (latency, average))

        gyro = sensors.gyro
        accel = sensors.accel
        flex = sensors.flex
        button = sensors.button

        gyro.pitch = scale_sensors(SCALE_RANGE, gyro.pitch, SENSOR_MAX_OF_GYRO, SENSOR_MIN_OF_GYRO, NEUTRAL_OF_PITCH)
        gyro.roll = scale_sensors(SCALE_RANGE, gyro.roll, SENSOR_MAX_OF_GYRO, SENSOR_MIN_OF_GYRO, NEUTRAL_OF_ROLL)
        gyro.yaw = scale_sensors(SCALE_RANGE, gyro.yaw, SENSOR_MAX_OF_GYRO, SENSOR_MIN_OF_GYRO, NEUTRAL_OF_YAW)

        gyro.yaw = deadzone(gyro.yaw, DEADZONE)
        gyro.pitch = deadzone(gyro.pitch, DEADZONE)

        #flex.thumb = scale_sensors(50, flex.thumb, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)
        #flex.index = scale_sensors(50, flex.index, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)
        #flex.middle = scale_sensors(50, flex.middle, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)
        #flex.ring = scale_sensors(50, flex.ring, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)
        #flex.pinky = scale_sensors(50, flex.pinky, SENSOR_MIN_OF_FLEX, SENSOR_MAX_OF_FLEX, NEUTRAL_OF_FLEX)

        # state = get_stated_based_on_flex(flex)
        state = get_flex_state(flex, prev_state)

        if button.pressed:
            state = RECENTER

        log.debug("State: " + str(state))

        if (state in [MOUSE_MODE, CLICK_MODE, RIGHT_CLICK_MODE]):
            if(state == CLICK_MODE):
                if prev_state != CLICK_MODE:
                    pyautogui.mouseDown()
            elif (state == RIGHT_CLICK_MODE):
                pyautogui.mouseDown(button='right')
            else:   # MOUSE_MODE
                if prev_state != MOUSE_MODE:
                    pyautogui.mouseUp()
                    pyautogui.mouseUp(button='right')

            # don't move cursor beyond screen limit
            cursor = pyautogui.position()
            dx = -gyro.yaw
            dy = -gyro.pitch

            if cursor.x + dx > maxWidth:
                dx = maxWidth - cursor.x
            elif cursor.x + dx < 0:
                dx = -cursor.x

            if cursor.y + dy > maxHeight:
                dy = maxHeight - cursor.y
            elif cursor.y + dy < 0:
                dy = -cursor.y

            pyautogui.move(dx, dy)

        elif state == SINGLE_CLICK_MODE:
            if(prev_state != SINGLE_CLICK_MODE):
                pyautogui.click()

        elif state == SCROLL_MODE:
            pitch = deadzone(gyro.pitch, 10)
            if pitch > 0:
                pyautogui.scroll(-1)
            elif pitch < 0:
                pyautogui.scroll(1)

        elif button.pressed:
            pyautogui.moveTo(maxWidth // 2, maxHeight // 2)

        else:
            log.debug("not in a recognizable state")

        prev_state = state
        #print(sensors)
        #agent.perform_action(state.lower())
