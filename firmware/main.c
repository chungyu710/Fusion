#include <xc.h>
#include <pic16f690.h>
#include <string.h>
#include <stdio.h>

#include "system.h"

#include "temp/uart.h"
#include "imu.h"

#include "tests/gyro.h"
#include "tests/accel.h"

void main(void)
{
	system_initialize();
	//test_gyro();
	test_accel();

	//imu_write_register(0x10, 0xDD);   // set accel settings
	//U8 value = imu_read_register(0x10);     // read back accel settings
	//printf("accel settings 0x%02X\r\n", value);

	printf("WHO_AM_I: 0x%02X\r\n", imu_read_register(0x0F));

	while (1)
	{
		_delay(100000);
	}
}
