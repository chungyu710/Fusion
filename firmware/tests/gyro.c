#include "tests/gyro.h"

#include <xc.h>
#include <stdio.h>

#include "drivers/gyro.h"

void test_gyro(void)
{
	gyro_set_range(GYRO_RANGE_125_DPS);

	while (1)
	{
		Gyro gyro;
		gyro_read(&gyro);
		printf("pitch: %d, roll: %d, yaw: %d\r\n", gyro.pitch, gyro.roll, gyro.yaw);
		_delay(10000);
	}
}
