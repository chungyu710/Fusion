import json

def get_states_from_json():
    with open("states.json", "r") as f:
        return json.load(f)
    
# accel: {"x": V, "y": V, "z": V}
# accel is expected to be a json object
def get_state_based_on_accel(accel):
    state_values = get_states_from_json()
    # States
    states=["START", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN"]
    for state in states:
        if (check_accel_values(state_values[state]['accel'], accel)):
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

