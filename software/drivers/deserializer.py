from drivers.common import *
from drivers.protocol import *

import serial
import log
import struct
import time
import signal

SERIAL_PORTS = {
    "wireless":
    {
        "left": "/dev/cu.fusion-left-DevB",
        "right": "/dev/cu.fusion-right-DevB"
    },
    "wired":
    {
        "left": "/dev/cu.usbserial-ABSCDXWM",
        "right": "/dev/cu.usbserial-ABSCDXWM"
    },
}

BAUDRATE = 115200   # UART baud rate
TIMEOUT_S = 1       # serial port timeout in seconds
RESET_DELAY_S = 2   # time to wait after issuing a reset so that MCU firmware can reboot
MAX_RETRIES = 5     # maximum times the glove is reset before giving up on the handshake
PURGE_SIZE = 1024   # number of bytes to read and discard at a time

ser = None    # serial port
pending = 0   # number of pending sensor packets (burst mode only)

def ctrl_c_handler(signum, frame):
    print()
    abort(SUCCESS)

def get_serial_port(hand, mode):
    if mode not in SERIAL_PORTS:
        log.error(f"No such mode '{mode}'")
        return
    if hand not in SERIAL_PORTS[mode]:
        log.error(f"No such hand '{hand}'")
        return

    port = SERIAL_PORTS[mode][hand]
    log.info(f"Select '{port}' for Fusion {mode} {hand} hand")
    return port

def open(port, sync = True):
    global ser
    try:
        ser = serial.Serial(
            port=port,
            baudrate=BAUDRATE,
            stopbits=serial.STOPBITS_ONE,
            timeout=TIMEOUT_S,
            bytesize=serial.EIGHTBITS
        )
    except Exception as e:
        log.error(f"Error opening serial port: {e}")
        abort(ERROR)

    signal.signal(signal.SIGINT, ctrl_c_handler)
    purge()
    log.success(f"Opened serial port '{port}'")

    if sync:
        handshake()

def close():
    purge()
    ser.close()
    log.success("Closed serial port")

def purge():
    while True:
        size = len(ser.read(PURGE_SIZE))
        if size == 0:
            break
        log.info(f"Discarding {size} B of remnant data")

    ser.reset_input_buffer()
    ser.reset_output_buffer()
    log.success("Purged serial port")

def abort(result):
    close()
    log.success("Ending program")
    exit(result)

def handshake():
    log.info("Initiating handshake")

    tries = 0
    while not ping():
        tries += 1
        log.warning(f"Ping attempt {tries} failed")
        if tries > MAX_RETRIES:
            log.error(f"Failed to establish serial link")
            abort(ERROR)
        log.info("Resetting Fusion")
        reset()
        purge()

    log.success(f"Established serial link")

def send(command):
    # little endian (<)
    ser.write(struct.pack("<B", command))
    ser.flush()

def verify_checksum(header, payload):
    checksum = header.status ^ header.size
    payload = bytes(payload)

    for i in range(header.size):
        checksum ^= payload[i]

    return checksum == header.checksum

def ping():
    log.debug("PING")
    send(Command.PING)

    response = get_response_data()
    if response is None or response.header.status != Status.SUCCESS:
        log.error("Received invalid ping response")
        return False

    log.success("Received valid ping response")
    return True

def reset():
    log.debug("RESET")
    send(Command.RESET)
    log.info("Waiting for Fusion to restart")
    time.sleep(RESET_DELAY_S)   # give the MCU time to restart the firmware

def parse_sensor_data(payload):
    sensors = Sensors()
    if len(payload) != sensors.SIZE:
        log.error(f"Incorrect payload size '{len(payload)} B' for sensor data ({sensors.SIZE} B)")
        abort(ERROR)
    sensors.unpack(payload)
    log.debug("------- SENSORS -------\r\n" + str(sensors))
    return sensors

def get_response_data():
    # Get the response header, should be Header.SIZE bytes
    header = Header()
    data = ser.read(Header.SIZE)

    if len(data) != Header.SIZE:
        log.error(f"Read {len(data)}/{Header.SIZE} B of header data")
        return None

    header.unpack(data)
    log.debug("------- HEADER -------\r\n" + str(header))

    payload = ser.read(header.size)

    if len(payload) != header.size:
        log.error(f"Read {len(payload)}/{header.size} B of payload data")
        return None

    if not verify_checksum(header, payload):
        log.error("Checksum mismatch")
        return None

    if header.status == Status.SUCCESS:
        log.debug("Status (0x%02X): SUCCESS" % (header.status))
    elif header.status == Status.ERROR:
        log.error("Status (0x%02X): ERROR" % (header.status))
    elif header.status == Status.LOW_BATTERY:
        battery = Battery()
        battery.unpack(payload)
        log.error("Status (0x%02X): LOW_BATTERY [%s]" % (header.status, str(battery)))
    else:
        log.warning("Status (0x%02X): UNKNOWN" % (header.status))

    return Response(header, payload)

def sample():
    log.debug("SAMPLE")
    send(Command.SAMPLE)

    response = get_response_data()
    if response is None or response.header.status != Status.SUCCESS:
        abort(ERROR)

    return parse_sensor_data(response.payload)

def burst():
    global pending
    if pending < BURST_SIZE:
        log.debug(f"Requesting {BURST_SIZE} sensor samples")
        log.debug("BURST")
        send(Command.BURST)
        pending += BURST_SIZE

    response = get_response_data()
    if response is None or response.header.status != Status.SUCCESS:
        abort(ERROR)

    sensors = parse_sensor_data(response.payload)
    log.debug("Received sensor data")
    pending -= 1
    return sensors

def battery():
    log.debug("BATTERY")
    send(Command.BATTERY)

    response = get_response_data()
    if response is None or response.header.status != Status.SUCCESS:
        abort(ERROR)

    battery = Battery()
    battery.unpack(response.payload)
    return battery

def dump():
    data = ser.read(128)
    if len(data) != 0:
        print(data.decode("ascii"), end = "")
