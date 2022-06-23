#include "gyro.h"

#include <xc.h>
#include <pic16f690.h>
#include <stddef.h>

#include "imu.h"
#include "system.h"

#define GYRO_RANGE_MASK         0xF3
#define GYRO_RANGE_OFFSET       2

#define GYRO_RANGE_MASK_125     0xFD

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

Status gyro_set_range(Gyro_Range range)
{
	if (range >= GYRO_RANGE_UNKNOWN)
	{
		return STATUS_ERROR;
	}

	U8 value = imu_read_register(CTRL2_G);

	if (range == GYRO_RANGE_125_DPS)
	{
		value |= ~GYRO_RANGE_MASK_125;   // force 125 DPS bit to 1
	}
	else
	{
		value &= GYRO_RANGE_MASK_125;   // clear 125 DPS bit
		value &= GYRO_RANGE_MASK;
		value |= (U8)(range << GYRO_RANGE_OFFSET);
	}

	imu_write_register(CTRL2_G, value);
	return STATUS_SUCCESS;
}
