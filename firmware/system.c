#include "system.h"

#include <xc.h>

#include "gpio.h"
#include "adc.h"
#include "led.h"
#include "temp/uart.h"   // TODO: Remove this once UART drivers are done (along with Makefile stuff)
#include "spi.h"
#include "imu.h"
#include "accel.h"
#include "gyro.h"

// ======= CONFIGURATION BITS ======= //

#pragma config FOSC = INTRCIO   // use internal oscillotor and use clock pins as GPIO
#pragma config WDTE = OFF       // disable watchdog timer
#pragma config PWRTE = OFF      // disable powerup timer
#pragma config MCLRE = OFF      // set MCLR pin as digital input (disable reset functionality)
#pragma config CP = OFF         // disable program memory protection
#pragma config CPD = OFF        // disable data memory protection
#pragma config BOREN = ON       // enable brownout reset (ensures that power-on reset works properly)
#pragma config IESO = OFF       // disable internal-external switchover
#pragma config FCMEN = OFF      // disable failsafe clock monitor

// ================================== //

#define LED_DELAY    200000
#define LED_BLINKS   3

void system_initialize(void)
{
	// OSCILLATOR //

	OSCCONbits.IRCF = 0b111;      // set clock frequency to 8 MHz
	OSCCONbits.SCS = 1;           // use internal oscillator as system clock
	OSCTUNEbits.TUN = 0b00000;    // use factory-calibrated frequency

	// PERIPHERALS //

	gpio_initialize();
	adc_initialize();
	spi_initialize();

	// DRIVERS //

	led_initialize();
	uart_initialize();
	imu_initialize();
	accel_initialize();
	gyro_initialize();

	// STARTUP INDICATOR //

	for (int i = 0; i < LED_BLINKS; i++)
	{
		led_on();
		_delay(LED_DELAY);
		led_off();
		_delay(LED_DELAY);
	}
}
