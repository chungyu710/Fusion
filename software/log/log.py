from .colours import *

def error(message):
	print(f"{RED}X{RESET} {message}")

def warning(message):
	print(f"{YELLOW}!{RESET} {message}")

def success(message):
	print(f"{GREEN}~{RESET} {message}")

def debug(message):
	print(f"{CYAN}#{RESET} {message}")

def info(message):
	print(f"{BLUE}>{RESET} {message}")

def note(message):
	print(f"{MAGENTA}@{RESET} {message}")
