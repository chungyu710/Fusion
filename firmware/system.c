#include "system.h"

#include <xc.h>

#include "led.h"

// CONFIGURATION BITS //

#pragma config FOSC = INTRCIO
#pragma config WDTE = OFF
#pragma config PWRTE = OFF
#pragma config MCLRE = OFF
#pragma config CP = OFF
#pragma config CPD = OFF
#pragma config BOREN = OFF
#pragma config IESO = OFF
#pragma config FCMEN = OFF

#define LED_DELAY   200000

static void startup_indicator(void)
{
	for (int i = 0; i < 3; i++)
	{
		led_on();
		_delay(LED_DELAY);
		led_off();
		_delay(LED_DELAY);
	}
}

void system_initialize(void)
{
	// INPUT (1) / OUTPUT (0) //

	TRISA = 0b00000000;
	TRISB = 0b00000000;
	TRISC = 0b00000000;

	// ANALOGUE (1) / DIGITAL (0) //

	ANSEL  = 0b00000000;
	ANSELH = 0b00000000;

	// initialize ports
	PORTA = 0b00000000;
	PORTB = 0b00000000;
	PORTC = 0b00000000;

	// OSCILLATOR FREQUENCY //

	OSCCONbits.IRCF = 0b111;      // Fosc = 8MHz
	OSCCONbits.SCS = 1;           // use internal oscillator
	OSCTUNEbits.TUN = 0b00000;    // use factory-calibrated frequency

	startup_indicator();
}
