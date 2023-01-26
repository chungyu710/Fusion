#include "spi.h"

#include <xc.h>
#include <stddef.h>

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
	TRIS_SDI = INPUT;
	TRIS_SDO = OUTPUT;
	TRIS_SS = OUTPUT;

	spi_release();

	// CONFIGURATION //

	/*
	The IMU uses SPI mode 3 (SCK idles high, clock out data on rising edge,
	clock in data on falling edge).  See page 14 of the IMU datasheet for
	the timing diagram.  The minimum SPI clock cycle for the IMU is 100 ns
	(1 GHz) which is much higher than Fosc.
	*/

	SSPSTATbits.SMP = 0;        // sample SDI at the middle of SDO cycle
	SSPSTATbits.CKE = 0;        // SDO driven on falling edge, SDI captured on rising edge
	SSPCONbits.CKP = 1;         // SCK idle high
	SSPCONbits.SSPM = 0b0000;   // SPI master mode at Fosc/4 (fastest speed)
	SSPCONbits.SSPEN = 1;       // enable SPI and configure SCK, SDI, and SDO
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
		system_abort(ABORT_NULL_POINTER);
	}

	char * bytes = (char *)data;
	char dummy = SSPBUF;   // read buffer to clear BF flag

	for (U8 i = 0; i < length; i++)
	{
		SSPBUF = bytes[i];            // write byte to buffer
		// TODO: check for write collision here
		while (SSPSTATbits.BF == 0);  // wait for next 8 bits to cycle through
		dummy = SSPBUF;               // read buffer to clear BF flag
	}
}

void spi_receive(void * data, U8 length)
{
	if (data == NULL)
	{
		system_abort(ABORT_NULL_POINTER);
	}

	char * bytes = (char *)data;
	char dummy = SSPBUF;   // read buffer to clear BF flag

	for (U8 i = 0; i < length; i++)
	{
		SSPBUF = 0;                    // write dummy byte to buffer
		// TODO: check for write collision here
		while (SSPSTATbits.BF == 0);   // wait for byte to be received
		bytes[i] = SSPBUF;             // save received byte
	}
}
