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
