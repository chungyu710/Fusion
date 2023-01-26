#include "accel.h"

#include <xc.h>
#include <stddef.h>

#include "imu.h"
#include "system.h"

#define ACCEL_RANGE_MASK     0xF3
#define ACCEL_RANGE_OFFSET   2

void accel_initialize(void)
{
	imu_write_register(CTRL1_XL, 0x42);   // enable accelerometer at 104 Hz with LPF2 and +/-2g
}

void accel_read(Accel * accel)
{
	if (accel == NULL)
	{
		system_abort(ABORT_NULL_POINTER);
	}

	/*
	The high register immediately follows the low register.
	Since the PIC is little endian, both these registers can
	be read and deciphered in a single SPI read command.
	In fact, all 3 axes can be read at once if the Sensor
	struct follows the correct order of the registers.
	*/

	imu_read(OUTX_L_A, accel, sizeof(*accel));
}

Status accel_set_range(Accel_Range range)
{
	if (range >= ACCEL_RANGE_UNKNOWN)
	{
		return STATUS_ERROR;
	}

	U8 value = imu_read_register(CTRL1_XL);
	value &= ACCEL_RANGE_MASK;
	value |= (U8)(range << ACCEL_RANGE_OFFSET);
	imu_write_register(CTRL1_XL, value);
	return STATUS_SUCCESS;
}
