#include "tests/gyro.h"

#include <xc.h>
#include <pic16f690.h>
#include <stdio.h>

#include "drivers/gyro.h"

void test_gyro(void)
{
	while (1)
	{
		Gyro gyro;
		gyro_read(&gyro);
		printf("pitch: %d, roll: %d, yaw: %d\r\n", gyro.pitch, gyro.roll, gyro.yaw);
		_delay(10000);
	}
}
