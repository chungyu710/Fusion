import log

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

LOG_SUPPRESSION = {
	"note":    0,
	"debug":   1,
	"info":    2,
	"success": 3,
	"warning": 4,
	"error":   5,
	"disable": 6,
}

def set_log_level(level):
	level = level.lower()
	if level not in LOG_SUPPRESSION:
		log.error(f"No such log level '{level}'")
		return

	# everything enabled by default
	log.success(f"Set log level to '{level}'")
	suppression = LOG_SUPPRESSION[level]

	if suppression > 0:
		log.suppress(log.Level.NOTE)
	if suppression > 1:
		log.suppress(log.Level.DEBUG)
	if suppression > 2:
		log.suppress(log.Level.INFO)
	if suppression > 3:
		log.suppress(log.Level.SUCCESS)
	if suppression > 4:
		log.suppress(log.Level.WARNING)
	if suppression > 5:
		log.suppress(log.Level.ERROR)
