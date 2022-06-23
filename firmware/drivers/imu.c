#include "imu.h"

#include <xc.h>
#include <pic16f690.h>

#include "spi.h"

void imu_initialize(void)
{
	// TODO: one-time register setup for IMU
}

U8 imu_read(U8 address)
{
	address |= 0x80;   // MSB of register address is 1
	spi_select();
	spi_transmit(&address, sizeof(address));
	U8 value;
	spi_receive(&value, sizeof(value));
	spi_release();
	return value;
}

// TODO: multi-byte read and write
void imu_write(U8 address, U8 data)
{
	// MSB of address is 0
	U8 packet [2];
	packet[0] = address;
	packet[1] = data;
	spi_select();
	spi_transmit(&packet, sizeof(packet));
	spi_release();
}
