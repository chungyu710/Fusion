#include <xc.h>
#include <pic16f690.h>
#include <string.h>
#include <stdio.h>

#include "system.h"

#include "temp/uart.h"
#include "spi.h"
#include "imu.h"

void main(void)
{
	system_initialize();

	uart_initialize();   // TODO: Remove this once UART drivers are done (along with Makefile stuff)

	U8 write = 0xFE;
	U8 read;
	imu_write(0x10, &write, 1);   // set accel settings
	imu_read(0x10, &read, 1);     // read back accel settings
	printf("accel settings 0x%02X\r\n", read);

	while (1)
	{
		imu_read(0x0F, &read, 1);
		printf("0x%02X\r\n", read);
		_delay(1000000);
	}
}
