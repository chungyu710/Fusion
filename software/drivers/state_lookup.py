import json
import log

def get_states_from_json():
    with open("calibartion.json", "r") as f:
        return json.load(f)

def get_states_from_calibration():
    with open("calibration.json", "r") as f:
        return json.load(f)

# accel: {"x": V, "y": V, "z": V}
# accel is expected to be a json object
def get_state_based_on_accel(accel):
    state_values = get_states_from_json()
    # States
    states=["START", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN"]

    for state in states:
        # if (check_accel_values(state_values[state]['accel'], accel) and
        #     check_gyro_values(...) and
        #     check_flex_values(...)):
        if check_accel_values(state_values[state]['accel'], accel):
            return state

    return "ERROR"



# expected format exmaple -> {'x': {'min': 10, 'max': 20}, 'y': {'min': 10, 'max': 20}, 'z': {'min': 10, 'max': 20}}
# sensor format exanple (expected to be json) -> {"x": V, "y": V, "z": V}
def check_accel_values(expected, accel):
    x_min = expected['x']['min']
    x_max = expected['x']['max']
    y_min = expected['y']['min']
    y_max = expected['y']['max']
    z_min = expected['z']['min']
    z_max = expected['z']['max']

    return ((accel.x >= x_min and accel.x <= x_max) and
            (accel.y >= y_min and accel.y <= y_max) and
            (accel.z >= z_min and accel.z <= z_max))

def get_stated_based_on_flex(flex):
    state_values = get_states_from_json()
    # States
    # each number represents finger from thumb to index
    # 00000 - enable 'mouse' mode
    # 01000 - hold down left click
    # 11000 - hold down right click
    # 10000 - double click (on release of thumb? as long as thumb is held out?)
    # 01110 - enable 'swipe' mode
    # 01100 - enable 'scroll' mode

    states=["00000", "01000", "01100", "10000", "01110", "11000"]

    for state in states:
        if check_flex_values(state_values[state]['flex'], flex):
            log.debug("state is " + state)
            return state

    return "ERROR"

def check_flex_values(expected, flex):
    thumb_min = expected['thumb']['min']
    thumb_max = expected['thumb']['max']
    index_min = expected['index']['min']
    index_max = expected['index']['max']
    middle_min = expected['middle']['min']
    middle_max = expected['middle']['max']
    ring_min = expected["ring"]["min"]
    ring_max = expected["ring"]["max"]
    pinky_min = expected['pinky']['min']
    pinky_max = expected['pinky']['max']

    return ((flex.thumb >= thumb_min and flex.thumb <= thumb_max) and
            (flex.index >= index_min and flex.index <= index_max) and
            (flex.middle >= middle_min and flex.middle <= middle_max) and
            (flex.ring >= ring_min and flex.ring <= ring_max) and
            (flex.pinky >= pinky_min and flex.pinky <= pinky_max))
    # return flex.index >= index_min and flex.index <= index_max

def get_flex_state(flex, prev_state = "00000"):
    # state_values = get_states_from_json()
    state_values = get_states_from_calibration()
    states = ["thumb_closed","index_closed","middle_closed","ring_closed","pinky_closed","thumb_open","index_open","middle_open","ring_open","pinky_open"]

    thumb = prev_state[0]
    index = prev_state[1]
    middle = prev_state[2]
    ring = prev_state[3]
    pinky = prev_state[4]

    if(flex.thumb >= state_values['thumb_closed']['min'] and flex.thumb <= state_values['thumb_closed']['max']):
        thumb = "0"
    elif(flex.thumb >= state_values['thumb_open']['min'] and flex.thumb <= state_values['thumb_open']['max']):
        thumb = "1"

    if(flex.index >= state_values['index_closed']['min'] and flex.index <= state_values['index_closed']['max']):
        index = "0"
    elif(flex.index >= state_values['index_open']['min'] and flex.index <= state_values['index_open']['max']):
        index = "1"

    if(flex.middle >= state_values['middle_closed']['min'] and flex.middle <= state_values['middle_closed']['max']):
        middle = "0"
    elif(flex.middle >= state_values['middle_open']['min'] and flex.middle <= state_values['middle_open']['max']):
        middle = "1"

    if(flex.ring >= state_values['ring_closed']['min'] and flex.ring <= state_values['ring_closed']['max']):
        ring = "0"
    elif(flex.ring >= state_values['ring_open']['min'] and flex.ring <= state_values['ring_open']['max']):
        ring = "1"

    if(flex.pinky >= state_values['pinky_closed']['min'] and flex.pinky <= state_values['pinky_closed']['max']):
        pinky = "0"
    elif(flex.pinky >= state_values['pinky_open']['min'] and flex.pinky <= state_values['pinky_open']['max']):
        pinky = "1"

    return thumb + index + middle + ring + pinky
