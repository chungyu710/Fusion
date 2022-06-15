# compiler / linker
CC = xc8-cc

# compiler / linker flags
FLAGS += -mcpu=16f690
FLAGS += -mc90lib

# linker libraries
LIBS +=

# source file directories
# NOTE: include paths are searched in this order
DIR += peripherals
DIR += drivers
DIR += tests

# artifacts folder
ART = build

# hex binary name
BIN = fusion
