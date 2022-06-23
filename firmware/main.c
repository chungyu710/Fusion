#include <xc.h>
#include <pic16f690.h>
#include <string.h>
#include <stdio.h>

#include "system.h"

#include "temp/uart.h"
#include "imu.h"

void main(void)
{
	system_initialize();

	uart_initialize();   // TODO: Remove this once UART drivers are done (along with Makefile stuff)

	//imu_write_register(0x10, 0xDD);   // set accel settings
	//U8 value = imu_read_register(0x10);     // read back accel settings
	//printf("accel settings 0x%02X\r\n", value);

	printf("WHO_AM_I: 0x%02X\r\n", imu_read_register(0x0F));

	while (1)
	{
		//printf("STATUS_REG: 0x%02X\r\n", imu_read_register(STATUS_REG));
		U8 high = imu_read_register(OUTX_H_A);
		U8 low = imu_read_register(OUTX_L_A);
		S16 x = ((S16)high << 8) | low;
		//printf("OUTX_H_A: 0x%02X\r\n", );
		//printf("OUTX_L_A: 0x%02X\r\n", );
		printf("X: %d\r\n", x);
		_delay(100000);
	}
}
