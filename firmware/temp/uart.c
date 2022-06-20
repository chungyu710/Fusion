#include "uart.h"

#include <xc.h>
#include <pic16f690.h>
#include <stddef.h>

void uart_initialize(void)
{
	RCSTAbits.SPEN = 1;
	RCSTAbits.RX9 = 0;
	RCSTAbits.CREN = 1;

	TXSTAbits.TX9 = 0;
	TXSTAbits.TXEN = 1;
	TXSTAbits.SYNC = 0;
	TXSTAbits.BRGH = 1;

	BAUDCTLbits.SCKP = 0;
	BAUDCTLbits.BRG16 = 1;
	BAUDCTLbits.WUE = 0;
	BAUDCTLbits.ABDEN = 0;

	//// 117647.058823529411765 bps @ 8 MHz (115200)
	SPBRGH = 0;
	SPBRG = 16;
}

void uart_transmit(void * data, U8 length)
{
	if (data == NULL)
	{
		return;
	}

	char * bytes = (char *)data;

	for (U8 i = 0; i < length; i++)
	{
		while (!TXSTAbits.TRMT);
		TXREG = bytes[i];
	}
}

void uart_receive(void * data, U8 length);

void putch(char byte)
{
	uart_transmit(&byte, 1);
}
