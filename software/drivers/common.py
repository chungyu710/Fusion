# Commands:
PING = b"\x00"
SENSORS_ALL = b"\x30"
SENSOR_ACCELEROMETER = b"\x31"

class Sensors:
    def __init__(self, accel, gyro, flex):
        self.accel = accel
        self.gyro =  gyro
        self.flex = flex

    def __str__(self):
        return str(self.accel) + str(self.gyro) + str(self.flex)

class Accelerometer:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y =  y
        self.z = z

    def __str__(self):
        return "Accelerometer values: " + " (x, y, z): (" + str(self.x) + ", " + str(self.y) + ", " +  str(self.z) + ")\n"

class Gyro:
    def __init__(self, pitch=0, yaw=0, roll=0):
        self.roll = roll
        self.pitch =  pitch
        self.yaw = yaw

    def __str__(self):
        return "Gyro values: " + " (roll, pitch, yaw): (" + str(self.roll) + ", " + str(self.pitch) + ", " +  str(self.yaw) + ")\n"


class Flex:
    def __init__(self, thumb=0, index=0, middle=0, ring=0, pinky=0):
        self.thumb = thumb
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky

    def __str__(self):
        return "Flex sensor values: " + " (thumb, index, middle, ring, pinky): (" + str(self.thumb) + ", " + str(self.index) + ", " +  str(self.middle) + ", " + str(self.ring) + ", " +  str(self.pinky) + ")\n"
