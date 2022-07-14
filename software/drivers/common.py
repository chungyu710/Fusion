# Commands:
PING = b"\x00"
SENSORS_ALL = b"\x30"
SENSOR_ACCELEROMETER = b"\x31"

class Sensors:
    def __init__(self, accel_data, gyro_data, flex_data):
        self.accel_data = accel_data
        self.gyro_data =  gyro_data
        self.flex_data = flex_data

    def __str__(self):
        return str(self.accel_data) + str(self.gyro_data) + str(self.flex_data)

class Accelerometer:
    def __init__(self, x, y, z):
        self.x = x
        self.y =  y
        self.z = z

    def __str__(self):
        return "Accelerometer values: " + " (x, y, z): (" + str(self.x) + ", " + str(self.y) + ", " +  str(self.z) + ")\n"

class Gyro:
    def __init__(self, pitch, yaw, roll):
        self.roll = roll
        self.pitch =  pitch
        self.yaw = yaw

    def __str__(self):
        return "Gyro values: " + " (roll, pitch, yaw): (" + str(self.roll) + ", " + str(self.pitch) + ", " +  str(self.yaw) + ")\n"


class Flex:
    def __init__(self, thumb, index, middle, ring, pinky):
        self.thumb = thumb
        self.index =  index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky

    def __str__(self):
        return "Flex sensor values: " + " (thumb, index, middle, ring, pinky): (" + str(self.thumb) + ", " + str(self.index) + ", " +  str(self.middle) + ", " + str(self.ring) + ", " +  str(self.pinky) + ")\n"
    