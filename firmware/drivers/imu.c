#include "imu.h"

#include <xc.h>
#include <pic16f690.h>
#include <stddef.h>

#include "spi.h"

void imu_initialize(void)
{
	// TODO: one-time register setup for IMU
}

void imu_read(U8 address, void * data, U8 length)
{
	if (data == NULL)
	{
		return;
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
		return;
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
