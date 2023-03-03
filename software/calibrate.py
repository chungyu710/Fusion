import argparse
from operator import iadd
import sys
from drivers import deserializer
from time import time, sleep

parser = argparse.ArgumentParser()
parser.add_argument('--log_level', default='INFO')
parser.add_argument('--port', required=True)
args = parser.parse_args()

deserializer.open(args.port)

MIN_VAL = -sys.maxsize
MAX_VAL = sys.maxsize
FIXED_BUFFER = 20

min_flex_closed_fist = [MAX_VAL, MAX_VAL, MAX_VAL, MAX_VAL, MAX_VAL]
max_flex_closed_fist = [MIN_VAL, MIN_VAL, MIN_VAL, MIN_VAL, MIN_VAL]

min_flex_open_fist = [MAX_VAL, MAX_VAL, MAX_VAL, MAX_VAL, MAX_VAL]
max_flex_open_fist = [MIN_VAL, MIN_VAL, MIN_VAL, MIN_VAL, MIN_VAL]

trials = 3
print("starting calibration for 5 seconds each trial ...; close fist; trials: " + str(trials))
sleep(2)

for i in range(trials):
    print("starting trial", i)

    start_time = time()
    while (time() - start_time < 5):
        sensors = deserializer.sample()
        # sensors = get_all_sensor_data(serial_port)

        min_flex_closed_fist[0] = min(min_flex_closed_fist[0], sensors.flex.thumb)
        min_flex_closed_fist[1] = min(min_flex_closed_fist[1], sensors.flex.index)
        min_flex_closed_fist[2] = min(min_flex_closed_fist[2], sensors.flex.middle)
        min_flex_closed_fist[3] = min(min_flex_closed_fist[3], sensors.flex.ring)
        min_flex_closed_fist[4] = min(min_flex_closed_fist[4], sensors.flex.pinky)

        max_flex_closed_fist[0] = max(max_flex_closed_fist[0], sensors.flex.thumb)
        max_flex_closed_fist[1] = max(max_flex_closed_fist[1], sensors.flex.index)
        max_flex_closed_fist[2] = max(max_flex_closed_fist[2], sensors.flex.middle)
        max_flex_closed_fist[3] = max(max_flex_closed_fist[3], sensors.flex.ring)
        max_flex_closed_fist[4] = max(max_flex_closed_fist[4], sensors.flex.pinky)

    # wait for 5 seconds
    if i == trials - 1:
        print("Waiting for 5 seconds - prepare for open fisting")
        sleep(5)
    else:
        print("Waiting for 5 seconds - do something else and get back to closing fist")
        sleep(5)

print("min_flex_closed_fist", min_flex_closed_fist)
print("max_flex_closed_fist", max_flex_closed_fist)

print("starting calibration for 5 seconds...; open fist")

for i in range(trials):
    print("starting trial", i)
    start_time = time()

    while (time() - start_time < 5):
        sensors = deserializer.sample()
        # sensors = get_all_sensor_data(serial_port)

        min_flex_open_fist[0] = min(min_flex_open_fist[0], sensors.flex.thumb)
        min_flex_open_fist[1] = min(min_flex_open_fist[1], sensors.flex.index)
        min_flex_open_fist[2] = min(min_flex_open_fist[2], sensors.flex.middle)
        min_flex_open_fist[3] = min(min_flex_open_fist[3], sensors.flex.ring)
        min_flex_open_fist[4] = min(min_flex_open_fist[4], sensors.flex.pinky)
        
        max_flex_open_fist[0] = max(max_flex_open_fist[0], sensors.flex.thumb)
        max_flex_open_fist[1] = max(max_flex_open_fist[1], sensors.flex.index)
        max_flex_open_fist[2] = max(max_flex_open_fist[2], sensors.flex.middle)
        max_flex_open_fist[3] = max(max_flex_open_fist[3], sensors.flex.ring)
        max_flex_open_fist[4] = max(max_flex_open_fist[4], sensors.flex.pinky)

    # wait for 5 seconds
    print("Waiting for 5 seconds - do something else and get back to open")
    sleep(5)

print("min_flex_open_fist", min_flex_open_fist)
print("min_flex_open_fist", min_flex_open_fist)

with open('calibration.json', 'w') as f:
    # write in the format as follows:
    # FIX - want no comma on last one for json format and want everything to be encased in {}
    """
    "thumb_open": {
        "max": 519,
        "min": 512
    },
    """
    fingers_closed = ["thumb_closed", "index_closed", "middle_closed", "ring_closed", "pinky_closed"]

    f.write("{")
    for i, finger_action in enumerate(fingers_closed):
        f.write('"' + finger_action + '": {\n')
        f.write('\t"max": ' + str(max_flex_closed_fist[i] + FIXED_BUFFER) + ',\n')
        f.write('\t"min": ' + str(min_flex_closed_fist[i] - FIXED_BUFFER) + '\n')
        f.write('},\n')

    fingers_open = ["thumb_open", "index_open", "middle_open", "ring_open", "pinky_open"]

    for i, finger_action in enumerate(fingers_open):
        f.write('"' + finger_action + '": {\n')
        f.write('\t"max": ' + str(max_flex_open_fist[i] + FIXED_BUFFER) + ',\n')
        f.write('\t"min": ' + str(min_flex_open_fist[i] - FIXED_BUFFER) + '\n')
        if i == len(fingers_open) - 1:
            f.write('}\n')
        else:
            f.write('},\n')

    f.write("}")