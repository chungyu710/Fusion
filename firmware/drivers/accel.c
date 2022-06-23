#include "accel.h"

#include <xc.h>
#include <pic16f690.h>
#include <stddef.h>

#include "imu.h"

void accel_initialize(void)
{
	imu_write_register(CTRL1_XL, 0x42);   // enable accelerometer at 104 Hz with LPF2 and +/-2g
}

void accel_read(Accel * accel)
{
	if (accel == NULL)
	{
		return;
	}

	/*
	The high register immediately follows the low register.
	Since the PIC is little endian, both these registers can
	be read and deciphered in a single SPI read command.
	In fact, all 3 axes can be read at once if the Sensor
	struct follows the correct order of the registers.
	*/

	imu_read(OUTX_L_A, accel, sizeof(Accel));
}

void accel_set_range(Accel_Range range);
