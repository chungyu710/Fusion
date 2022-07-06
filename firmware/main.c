#include <xc.h>
#include <pic16f690.h>
#include <stdio.h>

#include "system.h"

#include "tests/led.h"
#include "tests/uart.h"

void main(void)
{
	system_initialize();

	while(1) {
		test_uart_echo();
	}
}
