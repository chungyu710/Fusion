#include "system.h"

#include <xc.h>
#include <stddef.h>
#include <string.h>

#include "gpio.h"
#include "adc.h"
#include "led.h"
#include "uart.h"
#include "spi.h"
#include "imu.h"
#include "accel.h"
#include "gyro.h"
#include "link.h"
#include "button.h"
#include "battery.h"

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

#define LED_DELAY_US   200000
#define LED_BLINKS     3

static char * system_abort_reasons [ABORT_count] = {
	"NULL POINTER",
	"IMU OFFLINE",
	"LOW BATTERY",
};

void system_initialize(void)
{
	// OSCILLATOR //

	OSCCONbits.IRCF = 0b111;      // set clock frequency to 8 MHz
	OSCCONbits.SCS = 1;           // use internal oscillator as system clock
	OSCTUNEbits.TUN = 0b00000;    // use factory-calibrated frequency

	// INTERRUPTS //

	INTCONbits.PEIE = 1;   // enable peripherial interrupts

	// WATCHDOG //

	WDTCONbits.SWDTEN = 0;    // disable watchdog timer to prevent reset
	OPTION_REGbits.PSA = 1;   // assign prescaler to watchdog timer instead of Timer 0
	WDTCONbits.WDTPS = 0;     // set watchdog prescaler to fasest setting

	// PERIPHERALS //

	gpio_initialize();
	adc_initialize();
	spi_initialize();
	uart_initialize();

	// DRIVERS //

	led_initialize();
	imu_initialize();
	accel_initialize();
	gyro_initialize();
	flex_initialize();
	button_initialize();
	battery_initialize();

	// STARTUP INDICATOR //

	for (int i = 0; i < LED_BLINKS; i++)
	{
		led_on();
		_delay(LED_DELAY_US);
		led_off();
		_delay(LED_DELAY_US);
	}

	// ENABLE ALL INTERRUPTS //

	INTCONbits.GIE = 1;
}

void system_abort(Abort abort, char const * caller)
{
	while (button_released())
	{
		if (abort == ABORT_LOW_BATTERY)
		{
			led_pulse();   // Fade LED in and out during low battery.
		}
		else
		{
			led_blink();   // Blink LED during firmware errors.
		}

		if (abort < ABORT_count)
		{
			char * reason = system_abort_reasons[abort];
			char * newline = "\r\n";
			char * colon = ": ";

			if (caller != NULL)
			{
				uart_transmit(caller, strlen(caller));
				uart_transmit(colon, strlen(colon));
			}

			uart_transmit(reason, strlen(reason));
			uart_transmit(newline, strlen(newline));
		}
	}

	system_reboot();
}

void system_fatal(void)
{
	while (1)
	{
		led_blink_slow();
	}
}

void system_reboot(void)
{
	WDTCONbits.SWDTEN = 1;   // enable watchdog timer to force reset
}
