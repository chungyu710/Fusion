#include "system.h"

#include <xc.h>
#include <pic16f690.h>

#include "led.h"

// ======= CONFIGURATION BITS ======= //

#pragma config FOSC = INTRCIO   // use internal oscillotor and use clock pins as GPIO
#pragma config WDTE = OFF       // disable watchdog timer
#pragma config PWRTE = OFF      // disable powerup timer
#pragma config MCLRE = OFF      // set MCLR pin as digital input
#pragma config CP = OFF         // disable program memory protection
#pragma config CPD = OFF        // disable data memory protection
#pragma config BOREN = OFF      // disable brownout reset
#pragma config IESO = OFF       // disable internal-external switchover
#pragma config FCMEN = OFF      // disable failsafe clock monitor

// ================================== //

#define LED_DELAY    200000
#define LED_BLINKS   3

void system_initialize(void)
{
	// INPUT (1) / OUTPUT (0) //

	// set all pins out outputs
	TRISA = 0b00000000;
	TRISB = 0b00000000;
	TRISC = 0b00000000;

	// set all pins to 0 V
	PORTA = 0b00000000;
	PORTB = 0b00000000;
	PORTC = 0b00000000;

	// ANALOGUE (1) / DIGITAL (0) //

	// disable all ADC channels on pins
	ANSEL  = 0b00000000;
	ANSELH = 0b00000000;

	// OSCILLATOR //

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
