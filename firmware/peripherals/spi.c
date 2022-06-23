#include "spi.h"

#include <xc.h>
#include <pic16f690.h>
#include <stddef.h>









#include <stdio.h>

#include "system.h"

#define TRIS_SCK   TRISB6
#define TRIS_SDI   TRISB4
#define TRIS_SDO   TRISC7
#define TRIS_SS    TRISC6

#define SS   RC6

void spi_initialize(void)
{
	// GPIO //

	TRIS_SCK = OUTPUT;
	//TRIS_SDI = INPUT;
	TRIS_SDO = OUTPUT;
	TRIS_SS = OUTPUT;

	SS = 1;

	// CONFIGURATION //
//(SPI MODE 3)
// IMU sends and receives data on trailing failling edge cnad clock idles high
// page 14 of IMU datasheet shows slave timing
// SDO is driven on the falling edge, and SDI is captured on the rising edge
// minimum clock cycle is 100 ns -> 1 GHz max speed (Fosc = 8 MHz/4 so way under)
	SSPSTATbits.SMP = 0;   // sample SDI at the middle of SDO cycle
	SSPSTATbits.CKE = 0;   // SDO driven (data transmitted) on falling edge

	SSPCONbits.CKP = 1;      // SCK idle high
	SSPCONbits.SSPM = 0b0010;   // SPI master mode at Fosc/64 (slowest TODO: change later)
	SSPCONbits.SSPEN = 1;   // enable SPI and configure SCK, SDI, and SDO
}

void spi_select(void)
{
	SS = 0;
}

void spi_release(void)
{
	SS = 1;
}

void spi_transmit(void * data, U8 length)
{
	if (data == NULL)
	{
		return;
	}

	char * bytes = (char *)data;

	//SS = 0;

	for (U8 i = 0; i < length; i++)
	{
		char dummy = SSPBUF;   // read buffer to clear BF flag
		SSPBUF = bytes[i];     // write byte to buffer
		// TODO: check for write collision here
		while (SSPSTATbits.BF == 0)
		{
			printf("waiting for set BF TX 0x%x 0x%x 0x%x\r\n", bytes[i], SSPSTAT, SSPCON);
		}   // wait for next 8 bytes to cycle through
	}

	printf("TX finished 0x%x 0x%x\r\n", SSPSTAT, SSPCON);

	//SS = 1;
}

void spi_receive(void * data, U8 length)
{
	if (data == NULL)
	{
		return;
	}

	char * bytes = (char *)data;
	//SS = 0;

	for (U8 i = 0; i < length; i++)
	{
		while (SSPSTATbits.BF == 0)
		{
			printf("waiting for set BF RX 0x%x 0x%x\r\n", SSPSTAT, SSPCON);
			}   // wait for byte to be received
		printf("RX 0x%x 0x%x\r\n", SSPSTAT, SSPCON);
		bytes[i] = SSPBUF;   // read and save byte
		printf("RX 0x%x 0x%x\r\n", SSPSTAT, SSPCON);
	}

	//SS = 1;
}
