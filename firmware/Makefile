CC = xc8-cc

CCFLAGS += -mcpu=16F690
CCFLAGS += -mc90lib
#CCFLAGS += -mwarn=0

$(shell mkdir -p build)

build/fusion: hello.c
	$(CC) $(CCFLAGS) $^ -o $@

clean:
	rm -rvf build
