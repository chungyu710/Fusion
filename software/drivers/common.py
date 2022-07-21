from log import colours

# Commands:
PING = b"\x00"
SENSORS_ALL = b"\x30"
SENSOR_ACCELEROMETER = b"\x31"

def deadzone(value, radius):
	if abs(value) < 10:
		value = 0
	elif value > 0:
		value -= radius
	elif value < 0:
		value += radius
	return value

class Sensors:
    def __init__(self, accel, gyro, flex, button):
        self.accel = accel
        self.gyro =  gyro
        self.flex = flex
        self.button = button

    def __str__(self):
        return str(self.accel) + str(self.gyro) + str(self.flex) + str(self.button)

class Accelerometer:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y =  y
        self.z = z

    def __str__(self):
        return "%s%6s%s: %6.0f\r\n%s%6s%s: %6.0f\r\n%s%6s%s: %6.0f\r\n" % (
            colours.BLUE, "x", colours.RESET, self.x,
            colours.BLUE, "y", colours.RESET, self.y,
            colours.BLUE, "z", colours.RESET, self.z
        )

class Gyro:
    def __init__(self, pitch=0, yaw=0, roll=0):
        self.roll = roll
        self.pitch =  pitch
        self.yaw = yaw

    def __str__(self):
        return "%s%6s%s: %6.0f\r\n%s%6s%s: %6.0f\r\n%s%6s%s: %6.0f\r\n" % (
            colours.RED, "pitch", colours.RESET, self.pitch,
            colours.RED, "roll", colours.RESET, self.roll,
            colours.RED, "yaw", colours.RESET, self.yaw
        )


class Flex:
    def __init__(self, thumb=0, index=0, middle=0, ring=0, pinky=0):
        self.thumb = thumb
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky

    def __str__(self):
        return "%s%6s%s: %6.0f\r\n%s%6s%s: %6.0f\r\n%s%6s%s: %6.0f\r\n%s%6s%s: %6.0f\r\n%s%6s%s: %6.0f\r\n" % (
            colours.YELLOW, "thumb", colours.RESET, self.thumb,
            colours.YELLOW, "index", colours.RESET, self.index,
            colours.YELLOW, "middle", colours.RESET, self.middle,
            colours.YELLOW, "ring", colours.RESET, self.ring,
            colours.YELLOW, "pinky", colours.RESET, self.pinky
        )

class Button:
    def __init__(self, pressed=0):
        self.pressed = pressed

    def __str__(self):
        return "%s%6s%s: %6d\r\n" % (colours.GREEN, "button", colours.RESET, self.pressed)
