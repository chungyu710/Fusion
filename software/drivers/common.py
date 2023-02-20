ERROR = -1
SUCCESS = 0

def deadzone(value, radius):
	if abs(value) < radius:
		value = 0
	elif value > 0:
		value -= radius
	elif value < 0:
		value += radius
	return value
