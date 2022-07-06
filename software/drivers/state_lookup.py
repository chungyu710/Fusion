import json

# States
states=["START", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN"]

def get_states_from_json():
    with open("software/drivers/states.json", "r") as f:
        return json.load(f)
    
# "accel": {"x": V, "y": V, "z": V}
# accel is expected to be a json object
def get_state_based_on_accel(accel):
    state_values = get_states_from_json()
    
    for state in states:
        if (check_accel_values(state_values[state]['accel'], accel)):
            return state

    return "ERROR"

# expected format exmaple -> {'x': {'min': 10, 'max': 20}, 'y': {'min': 10, 'max': 20}, 'z': {'min': 10, 'max': 20}}
# sensor format exanple (expected to be json) -> "accel": {"x": V, "y": V, "z": V}
def check_accel_values(expected, sensor):
    x_min = expected['x']['min']
    x_max = expected['x']['max']
    y_min = expected['y']['min']
    y_max = expected['y']['max']
    z_min = expected['z']['min']
    z_max = expected['z']['max']

    return ((sensor['x'] >= x_min and sensor['x'] <= x_max) and 
            (sensor['y'] >= y_min and sensor['y'] <= y_max) and 
            (sensor['z'] >= z_min and sensor['z'] <= z_max))

