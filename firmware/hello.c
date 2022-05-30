#include <xc.h>
#include <pic16f690.h>

#pragma config FOSC = INTRCIO
#pragma config WDTE = OFF
#pragma config PWRTE = OFF
#pragma config MCLRE = OFF
#pragma config CP = OFF
#pragma config CPD = OFF
#pragma config BOREN = OFF
#pragma config IESO = OFF
#pragma config FCMEN = OFF

void main(void)
{
	TRISCbits.TRISC4 = 0;

	while (1)
	{
		RC4 = 1;
		_delay(1000000);
		RC4 = 0;
		_delay(1000000);
	}
}
