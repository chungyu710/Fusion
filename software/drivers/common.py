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
        return f"{str(self.accel)}\n{str(self.gyro)}\n{str(self.flex)}\n{str(self.button)}\n"

class Accelerometer:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y =  y
        self.z = z

    def __str__(self):
        return "| %sx%s: %6.0f | %sy%s: %6.0f | %sz%s: %6.0f |" % (
            colours.BLUE, colours.RESET, self.x,
            colours.BLUE, colours.RESET, self.y,
            colours.BLUE, colours.RESET, self.z
        )

class Gyro:
    def __init__(self, pitch=0, yaw=0, roll=0):
        self.roll = roll
        self.pitch =  pitch
        self.yaw = yaw

    def __str__(self):
        return "| %spitch%s: %6.0f | %sroll%s: %6.0f | %syaw%s: %6.0f |" % (
            colours.RED, colours.RESET, self.pitch,
            colours.RED, colours.RESET, self.roll,
            colours.RED, colours.RESET, self.yaw
        )


class Flex:
    def __init__(self, thumb=0, index=0, middle=0, ring=0, pinky=0):
        self.thumb = thumb
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky

    def __str__(self):
        return "| %sthumb%s: %4.0f | %sindex%s: %4.0f | %smiddle%s: %4.0f | %sring%s: %4.0f | %spinky%s: %4.0f |" % (
            colours.YELLOW, colours.RESET, self.thumb,
            colours.YELLOW, colours.RESET, self.index,
            colours.YELLOW, colours.RESET, self.middle,
            colours.YELLOW, colours.RESET, self.ring,
            colours.YELLOW, colours.RESET, self.pinky
        )

class Button:
    def __init__(self, pressed=0):
        self.pressed = pressed

    def __str__(self):
        return "| %sbutton%s: %d |" % (colours.GREEN, colours.RESET, self.pressed)
