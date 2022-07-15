import log
from time import time
from drivers.common import *

v0 = Accelerometer()
t0 = time()

def deadzone(value, radius):
	if abs(value) < 10:
		value = 0
	elif value > 0:
		value -= radius
	elif value < 0:
		value += radius
	return value

def calculate_velocity(a):
	global v0
	global t0

	t = time()
	dt = t - t0
	log.debug(dt)
	v = Accelerometer()

	v.x = v0.x + (a.x * dt)
	v.y = v0.y + (a.y * dt)
	v.z = v0.z + (a.z * dt)

	v0 = v
	t0 = t

	return v
