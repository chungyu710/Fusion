import struct

from log import colours
from enum import IntEnum

class Command(IntEnum):
    PING        = 0x00
    ACCEL_RANGE = 0x10
    GYRO_RANGE  = 0x20
    SAMPLE      = 0x30
    BATTERY     = 0x40
    RESET       = 0x50
    BURST       = 0x60

class Sensor_Group(IntEnum):
    ALL    = 0x0
    ACCEL  = 0x1
    GYRO   = 0x2
    FLEX   = 0x3
    BUTTON = 0x4

class Status(IntEnum):
    SUCCESS     = 0x0
    ERROR       = 0x1
    LOW_BATTERY = 0x2

BURST_SIZE = 5

class Response:
    def __init__(self, header = None, payload = None):
        self.header = header
        self.payload = payload

class Header:
    FORMAT = "BBB"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, status = 0, size = 0, checksum = 0):
        self.status = status
        self.size = size
        self.checksum = checksum

    def __str__(self):
        string = ""
        string += "%s%8s%s: %u\r\n" % (colours.MAGENTA, "status", colours.RESET, self.status)
        string += "%s%8s%s: %u\r\n" % (colours.MAGENTA, "size", colours.RESET, self.size)
        string += "%s%8s%s: 0x%X\r\n" % (colours.MAGENTA, "checksum", colours.RESET, self.checksum)
        return string

    def unpack(self, data, offset = 0):
        # little endian
        fields = struct.unpack_from(f"<{Header.FORMAT}", data, offset)
        self.status = fields[0]
        self.size = fields[1]
        self.checksum = fields[2]

class Accel:
    FORMAT = "hhh"
    SIZE = struct.calcsize(FORMAT)

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

    def unpack(self, data, offset = 0):
        # little endian
        fields = struct.unpack_from(f"<{Accel.FORMAT}", data, offset)
        self.x = fields[0]
        self.y = fields[1]
        self.z = fields[2]

class Gyro:
    FORMAT = "hhh"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, pitch = 0, yaw = 0, roll = 0):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw

    def __str__(self):
        string = ""
        string += "%s%6s%s: %6.0f\r\n" % (colours.RED, "pitch", colours.RESET, self.pitch,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.RED, "roll", colours.RESET, self.roll,)
        string += "%s%6s%s: %6.0f\r\n" % (colours.RED, "yaw", colours.RESET, self.yaw)
        return string

    def unpack(self, data, offset = 0):
        # little endian
        fields = struct.unpack_from(f"<{Gyro.FORMAT}", data, offset)
        self.pitch = fields[0]
        self.roll = fields[1]
        self.yaw = fields[2]

class Flex:
    FORMAT = "HHHHH"
    SIZE = struct.calcsize(FORMAT)

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

    def unpack(self, data, offset = 0):
        # little endian
        fields = struct.unpack_from(f"<{Flex.FORMAT}", data, offset)
        self.thumb = fields[0]
        self.index = fields[1]
        self.middle = fields[2]
        self.ring = fields[3]
        self.pinky = fields[4]

class Button:
    FORMAT = "B"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, pressed = 0):
        self.pressed = pressed

    def __str__(self):
        return "%s%6s%s: %6d\r\n" % (colours.GREEN, "button", colours.RESET, self.pressed)

    def unpack(self, data, offset = 0):
        # little endian
        fields = struct.unpack_from(f"<{Button.FORMAT}", data, offset)
        self.pressed = fields[0]

class Sensors:
    SIZE = Accel.SIZE + Gyro.SIZE + Flex.SIZE + Button.SIZE

    def __init__(self, accel = None, gyro = None, flex = None, button = None):
        self.accel = accel
        self.gyro =  gyro
        self.flex = flex
        self.button = button

    def __str__(self):
        return str(self.accel) + str(self.gyro) + str(self.flex) + str(self.button)

    def unpack(self, data, offset = 0):
        self.accel = Accel()
        self.accel.unpack(data, offset)
        offset += Accel.SIZE

        self.gyro = Gyro()
        self.gyro.unpack(data, offset)
        offset += Gyro.SIZE

        self.flex = Flex()
        self.flex.unpack(data, offset)
        offset += Flex.SIZE

        self.button = Button()
        self.button.unpack(data, offset)
        offset += Button.SIZE

class Battery:
    FORMAT = "H"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, voltage = 0):
        self.voltage = voltage

    def __str__(self):
        return "%s%8s%s: %.3f V" % (colours.RED, "voltage", colours.RESET, self.voltage)

    def unpack(self, data, offset = 0):
        # little endian
        fields = struct.unpack_from(f"<{Battery.FORMAT}", data, offset)
        self.voltage = fields[0] / 1000.0
