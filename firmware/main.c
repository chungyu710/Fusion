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
	RC6 = 1;
	_delay(100);

	char test = SSPBUF;   // read buffer to clear BF flag
	while (SSPSTATbits.BF == 1);
	_delay(100);

	RC6 = 0;

	SSPBUF = 0b00001010;     // write byte to buffer
	while (SSPSTATbits.BF == 0);

	U8 data = SSPBUF;   // read buffer to clear BF flag
	while (SSPSTATbits.BF == 1);

	SSPBUF = 0b01000000;     // write reg data
	while (SSPSTATbits.BF == 0);

	data = SSPBUF;   // read buffer to clear BF flag
	while (SSPSTATbits.BF == 1);

	RC6 = 1;
	_delay(1000000);

	// read back

	RC6 = 0;

	SSPBUF = 0b10001010;     // read byte from buffer
	while (SSPSTATbits.BF == 0);

	data = SSPBUF;   // read buffer to clear BF flag
	while (SSPSTATbits.BF == 1);

	SSPBUF = 0b00000000;     // write dummy byte to buffer
	while (SSPSTATbits.BF == 0);

	data = SSPBUF;   // read buffer to clear BF flag
	while (SSPSTATbits.BF == 1);
	printf("accel settings 0x%02x\r\n", data);

	RC6 = 1;
	_delay(1000000);


	while (1)
	{
		//U8 address = 0b10100010;
		U8 data = 0xFF;
		//spi_select();
		//spi_transmit(&address, 1);
		//spi_receive(&data, 1);
		//spi_release();
		//printf("%x\r\n", data);
		//_delay(1000000);

		//RC6 = 0;

		//SSPBUF = 0b10100001;     // write byte to buffer
		//while (SSPSTATbits.BF == 0);

		//_delay(10000);

		//data = SSPBUF;   // read buffer to clear BF flag
		//while (SSPSTATbits.BF == 1);

		//_delay(10000);

		//SSPBUF = 0b00000000;     // write dummy byte to buffer
		//while (SSPSTATbits.BF == 0);

		//_delay(10000);

		//data = SSPBUF;   // read buffer to clear BF flag
		//while (SSPSTATbits.BF == 1);
		//printf("RX %x\r\n", data);

		//_delay(1000000);

		//RC6 = 1;
		//_delay(1000000);


		// read back

		RC6 = 0;

		//SSPBUF = 0b10101000;     // read byte from buffer
		SSPBUF = 0b10001111;     // read byte from buffer
		while (SSPSTATbits.BF == 0);

		data = SSPBUF;   // read buffer to clear BF flag
		while (SSPSTATbits.BF == 1);

		SSPBUF = 0b00000000;     // write dummy byte to buffer
		while (SSPSTATbits.BF == 0);

		data = SSPBUF;   // read buffer to clear BF flag
		while (SSPSTATbits.BF == 1);
		printf("accelX 0x%02x\r\n", data);

		RC6 = 1;
		_delay(1000000);
	}
}
