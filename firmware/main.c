#include <xc.h>
#include <pic16f690.h>
#include <string.h>
#include <stdio.h>

#include "system.h"

#include "temp/uart.h"
#include "spi.h"

void main(void)
{
	system_initialize();

	uart_initialize();

	// set accel settings
	spi_select();
	U8 write_address = 0b00001010;
	U8 write_data = 0xAB;
	U8 packet [2];
	packet[0] = write_address;
	packet[1] = write_data;
	spi_transmit(&packet, sizeof(packet));
	spi_release();

	// read back accel settings
	spi_select();
	U8 read_address = write_address | 0x80;
	U8 read_data;
	spi_transmit(&read_address, sizeof(read_address));
	spi_receive(&read_data, sizeof(read_data));
	printf("accel settings 0x%02x\r\n", read_data);
	spi_release();

	while (1)
	{
		U8 address = 0b10001111;   // who am i
		U8 data = 0xFF;
		spi_select();
		spi_transmit(&address, 1);
		spi_receive(&data, 1);
		spi_release();
		printf("0x%02x\r\n", data);
		_delay(1000000);
	}
}
