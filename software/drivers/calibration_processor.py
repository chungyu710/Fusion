# range: value that the sensor reading should be scaled to (ex: 100 for -50 to 50)
# sensor_reading: value read from the sensor
# sensor_max: realistic highest sensor value
# sensor_min: realistic lowest sensor value
# centre: idle/neutral value from sensor
def scale_sensors (range, sensor_reading, sensor_max, sensor_min, centre):
    return range * (((sensor_reading - centre)) / (sensor_max - sensor_min))