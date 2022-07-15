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
    def __init__(self, accel, gyro, flex):
        self.accel = accel
        self.gyro =  gyro
        self.flex = flex

    def __str__(self):
        return f"{str(self.accel)}\n{str(self.gyro)}\n{str(self.flex)}\n"

class Accelerometer:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y =  y
        self.z = z

    def __str__(self):
        return "| %sX%s: %6.0f | %sY%s: %6.0f | %sZ%s: %6.0f |" % (
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
        return "| %sPITCH%s: %6.0f | %sROLL%s: %6.0f | %sYAW%s: %6.0f |" % (
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
        return "| %sTHUMB%s: %4.0f | %sINDEX%s: %4.0f | %sMIDDLE%s: %4.0f | %sRING%s: %4.0f | %sPINKY%s: %4.0f |" % (
            colours.YELLOW, colours.RESET, self.thumb,
            colours.YELLOW, colours.RESET, self.index,
            colours.YELLOW, colours.RESET, self.middle,
            colours.YELLOW, colours.RESET, self.ring,
            colours.YELLOW, colours.RESET, self.pinky
        )
