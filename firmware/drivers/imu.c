#include "imu.h"

#include <xc.h>
#include <stddef.h>

#include "spi.h"
#include "system.h"
#include "led.h"

#define BOOT_DELAY_US   10000

void imu_initialize(void)
{
	imu_write_register(CTRL3_C, 0x01);   // reset the IMU and set all registers to their default value
	_delay(BOOT_DELAY_US);               // Allow IMU to boot before reading the WHO_AM_I register

	// WHO_AM_I is hardcoded to 0x6C on the IMU
	if (imu_read_register(WHO_AM_I) != 0x6C)
	{
		ABORT(ABORT_IMU_OFFLINE);
	}
}

void imu_read(U8 address, void * data, U8 length)
{
	if (data == NULL)
	{
		ABORT(ABORT_NULL_POINTER);
	}

	address |= 0x80;   // MSB of register address is 1

	spi_select();
	spi_transmit(&address, 1);
	spi_receive(data, length);
	spi_release();
}

void imu_write(U8 address, void * data, U8 length)
{
	if (data == NULL)
	{
		ABORT(ABORT_NULL_POINTER);
	}

	address &= 0x7F;   // MSB of address is 0

	spi_select();
	spi_transmit(&address, 1);
	spi_transmit(data, length);
	spi_release();
}

U8 imu_read_register(U8 address)
{
	U8 data;
	imu_read(address, &data, 1);
	return data;
}

void imu_write_register(U8 address, U8 value)
{
	imu_write(address, &value, 1);
}
