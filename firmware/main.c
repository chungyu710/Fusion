#include <xc.h>
#include <stdio.h>

#include "system.h"

#include "imu.h"

#include "tests/gyro.h"
#include "tests/accel.h"
#include "tests/led.h"

void main(void)
{
	system_initialize();
	//test_gyro();
	//test_accel();

	//printf("WHO_AM_I: 0x%02X\r\n", imu_read_register(WHO_AM_I));

	test_led();
}
