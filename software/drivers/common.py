def deadzone(value, radius):
	if abs(value) < 10:
		value = 0
	elif value > 0:
		value -= radius
	elif value < 0:
		value += radius
	return value
