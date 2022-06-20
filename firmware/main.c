#include <xc.h>
#include <pic16f690.h>
#include <string.h>
#include <stdio.h>

#include "system.h"

#include "temp/uart.h"

void main(void)
{
	system_initialize();

	uart_initialize();

	while (1)
	{

	}
}
