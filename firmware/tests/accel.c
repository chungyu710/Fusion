#include "tests/accel.h"

#include <xc.h>
#include <stdio.h>

#include "drivers/accel.h"

void test_accel(void)
{
	accel_set_range(ACCEL_RANGE_2G);

	while (1)
	{
		Accel accel;
		accel_read(&accel);
		printf("X: %d, Y: %d, Z: %d\r\n", accel.x, accel.y, accel.z);
		_delay(10000);
	}
}
