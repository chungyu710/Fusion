#include <xc.h>
#include <pic16f690.h>
#include <string.h>
#include <stdio.h>

#include "system.h"

#include "temp/uart.h"
#include "imu.h"
#include "accel.h"

void main(void)
{
	system_initialize();

	//imu_write_register(0x10, 0xDD);   // set accel settings
	//U8 value = imu_read_register(0x10);     // read back accel settings
	//printf("accel settings 0x%02X\r\n", value);

	printf("WHO_AM_I: 0x%02X\r\n", imu_read_register(0x0F));

	while (1)
	{
		Accel accel;
		accel_read(&accel);
		printf("X: %d, Y: %d, Z: %d\r\n", accel.x, accel.y, accel.z);
		_delay(100000);
	}
}
