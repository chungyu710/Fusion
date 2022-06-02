#include "system.h"

#include <xc.h>
#include <pic16f690.h>

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

#define LED_DELAY    200000
#define LED_BLINKS   3

void system_initialize(void)
{
	// INPUT (1) / OUTPUT (0) //

	// set all pins out outputs
	TRISA = 0b00000000;
	TRISB = 0b00000000;
	TRISC = 0b00000000;

	// clear all pins
	PORTA = 0b00000000;
	PORTB = 0b00000000;
	PORTC = 0b00000000;

	// ANALOGUE (1) / DIGITAL (0) //

	// disable all ADC channels
	ANSEL  = 0b00000000;
	ANSELH = 0b00000000;

	// OSCILLATOR FREQUENCY //

	OSCCONbits.IRCF = 0b111;      // set clock frequency to 8 MHz
	OSCCONbits.SCS = 1;           // use internal oscillator as system clock
	OSCTUNEbits.TUN = 0b00000;    // use factory-calibrated frequency

	// STARTUP INDICATOR //

	for (int i = 0; i < LED_BLINKS; i++)
	{
		led_on();
		_delay(LED_DELAY);
		led_off();
		_delay(LED_DELAY);
	}
}
