import inspect

from . import colours
from enum import Enum

# ===================== LEVELS ===================== #

class Level(Enum):
	ERROR = 0
	WARNING = 1
	SUCCESS = 2
	DEBUG = 3
	INFO = 4
	NOTE = 5

	def list():
		return ["Level.ERROR", "Level.WARNING", "Level.SUCCESS", "Level.DEBUG", "Level.INFO", "Level.NOTE"]

# ===================== CONSTANTS ===================== #

COLOURS = {
	Level.ERROR:   colours.RED,
	Level.WARNING: colours.YELLOW,
	Level.SUCCESS: colours.GREEN,
	Level.DEBUG:   colours.CYAN,
	Level.INFO:    colours.BLUE,
	Level.NOTE:    colours.MAGENTA
}

PREFIXES = {
	Level.ERROR:   "X",
	Level.WARNING: "!",
	Level.SUCCESS: "~",
	Level.DEBUG:   "#",
	Level.INFO:    ">",
	Level.NOTE:    "@"
}

# ===================== FLAGS ===================== #

SUPPRESSED = {
	Level.ERROR:   False,
	Level.WARNING: False,
	Level.SUCCESS: False,
	Level.DEBUG:   False,
	Level.INFO:    False,
	Level.NOTE:    False
}

class Trace(Enum):
	FILE = 0
	LINE = 1
	CALLER = 2
	MODULE = 3

TRACE = {
	Trace.FILE:   False,
	Trace.LINE:   False,
	Trace.CALLER: False,
	Trace.MODULE: False
}

class Enable(Enum):
	LOGS = 0
	TRACE = 1
	COLOUR = 2

ENABLE = {
	Enable.LOGS:   True,
	Enable.TRACE:  False,
	Enable.COLOUR: True
}

# ===================== INTERNAL FUNCTIONS ===================== #

STACK_DEPTH = 4

def __trace():
	if not ENABLE[Enable.TRACE]:
		return ""

	stack = inspect.stack()
	file = ""
	line = ""
	caller = ""
	module = ""

	if TRACE[Trace.FILE]:
		file = f"{stack[STACK_DEPTH].filename}:"
	if TRACE[Trace.LINE]:
		line = f"{stack[STACK_DEPTH].lineno}:"
	if TRACE[Trace.CALLER]:
		caller = f"{stack[STACK_DEPTH].function}:"
	if TRACE[Trace.MODULE]:
		module = f"[{stack[STACK_DEPTH].frame.f_globals['__name__']}]"

	return f"{file}{line}{caller}{module} "

def __prefix(level):
	if ENABLE[Enable.COLOUR]:
		return f"{COLOURS[level]}{PREFIXES[level]}{colours.RESET} "
	else:
		return f"{PREFIXES[level]} "

def __format(level, message):
	return f"{__prefix(level)}{__trace()}{str(message)}\r\n"

def __invalid(level):
	print(f"'{level}' is an invalid log level")
	print(f"Valid log levels: {Level.list()}")

def __print(level, message):
	if SUPPRESSED[level] or not ENABLE[Enable.LOGS]:
		return
	print(__format(level, message), end = "")

# ===================== LOGGING API ===================== #

def enable():
	ENABLE[Enable.LOGS] = True

def disable():
	ENABLE[Enable.LOGS] = False

def suppress(level):
	if level in Level:
		SUPPRESSED[level] = True
	else:
		__invalid(level)
		raise Exception("Invalid log level")

def show(level):
	if level in Level:
		SUPPRESSED[level] = False
	else:
		__invalid(level)
		raise Exception("Invalid log level")

def colourize():
	ENABLE[Enable.COLOUR] = True

def colourless():
	ENABLE[Enable.COLOUR] = False

def trace(file = False, line = False, caller = False, module = False):
	TRACE[Trace.FILE] = file
	TRACE[Trace.LINE] = line
	TRACE[Trace.CALLER] = caller
	TRACE[Trace.MODULE] = module

	if file or line or caller or module:
		ENABLE[Enable.TRACE] = True
	else:
		ENABLE[Enable.TRACE] = False

def error(message):
	__print(Level.ERROR, message)

def warning(message):
	__print(Level.WARNING, message)

def success(message):
	__print(Level.SUCCESS, message)

def debug(message):
	__print(Level.DEBUG, message)

def info(message):
	__print(Level.INFO, message)

def note(message):
	__print(Level.NOTE, message)
