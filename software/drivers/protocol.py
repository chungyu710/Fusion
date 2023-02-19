from log import colours

COMMANDS = {
	"PING":        0x00,
	"ACCEL_RANGE": 0x10,
	"GYRO_RANGE":  0x20,
	"SENSORS":     0x30,
	"BATTERY":     0x40,
	"RESET":       0x50,
	"STREAM":      0x60
}

SENSOR_GROUPS = {
	"ALL":    0x0,
	"ACCEL":  0x1,
	"GYRO":   0x2,
	"FLEX":   0x3,
	"BUTTON": 0x4
}

STREAM_COMMANDS = {
	"START": 0x0,
	"STOP":  0x1
}

STATUS = {
	"SUCCESS":     0x0,
	"ERROR":       0x1,
	"LOW_BATTERY": 0x2
}

RESPONSE_HEADER_SIZE = 3 # bytes

class Response:
    def __init__(self, status = 0, length = 0, checksum = 0):
        self.status = status
        self.length = length
        self.checksum = checksum

    def __str__(self):
        string = ""
        string += "%s%8s%s: %u\r\n" % (colours.MAGENTA, "status", colours.RESET, self.status)
        string += "%s%8s%s: %u\r\n" % (colours.MAGENTA, "length", colours.RESET, self.length)
        string += "%s%8s%s: 0x%X\r\n" % (colours.MAGENTA, "checksum", colours.RESET, self.checksum)
        return string

class Sensors:
    def __init__(self, accel, gyro, flex, button):
        self.accel = accel
        self.gyro =  gyro
        self.flex = flex
        self.button = button

    def __str__(self):
        return str(self.accel) + str(self.gyro) + str(self.flex) + str(self.button)

class Accelerometer:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        string = ""
        string += "%s%6s%s: %6.0f\r\n" % (colours.BLUE, "x", colours.RESET, self.x,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.BLUE, "y", colours.RESET, self.y,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.BLUE, "z", colours.RESET, self.z)
        return string

class Gyro:
    def __init__(self, pitch = 0, yaw = 0, roll = 0):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def __str__(self):
        string = ""
        string += "%s%6s%s: %6.0f\r\n" % (colours.RED, "pitch", colours.RESET, self.pitch,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.RED, "roll", colours.RESET, self.roll,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.RED, "yaw", colours.RESET, self.yaw)
        return string

class Flex:
    def __init__(self, thumb = 0, index = 0, middle = 0, ring = 0, pinky = 0):
        self.thumb = thumb
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky

    def __str__(self):
        string = ""
        string += "%s%6s%s: %6.0f\r\n" % (colours.YELLOW, "thumb", colours.RESET, self.thumb,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.YELLOW, "index", colours.RESET, self.index,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.YELLOW, "middle", colours.RESET, self.middle,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.YELLOW, "ring", colours.RESET, self.ring,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.YELLOW, "pinky", colours.RESET, self.pinky)
        return string

class Button:
    def __init__(self, pressed = 0):
        self.pressed = pressed

    def __str__(self):
        return "%s%6s%s: %6d\r\n" % (colours.GREEN, "button", colours.RESET, self.pressed)
