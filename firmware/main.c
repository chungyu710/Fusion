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

	printf("WHO_AM_I: 0x%02X\r\n", imu_read_register(0x0F));

	while (1)
	{
		_delay(10000);
	}
}
