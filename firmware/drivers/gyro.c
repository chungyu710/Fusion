#include "gyro.h"

#include <xc.h>
#include <pic16f690.h>
#include <stddef.h>

#include "imu.h"

void gyro_initialize(void)
{
	imu_write_register(CTRL2_G, 0x40);   // enable gyroscope at 104 Hz at 250 dps
}

void gyro_read(Gyro * gyro)
{
	if (gyro == NULL)
	{
		return;
	}

	// See notes in accel.c about reading all axes at once.

	imu_read(OUTX_L_G, gyro, sizeof(Gyro));
}

void gyro_set_range(Gyro_Range range);
