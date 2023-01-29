#include "led.h"

#include <xc.h>

#include "system.h"

#define LED        RA5
#define TRIS_LED   TRISA5

#define BLINK_DELAY_US        500000
#define SLOW_BLINK_DELAY_US   2000000
#define PULSE_DELAY_US        10

void led_initialize(void)
{
	TRIS_LED = OUTPUT;
}

void led_on(void)
{
	LED = 1;
}

void led_off(void)
{
	LED = 0;
}

void led_blink(void)
{
	led_on();
	_delay(BLINK_DELAY_US);
	led_off();
	_delay(BLINK_DELAY_US);
}

void led_blink_slow(void)
{
	led_on();
	_delay(SLOW_BLINK_DELAY_US);
	led_off();
	_delay(SLOW_BLINK_DELAY_US);
}

static void pulse(U8 brightness)
{
	led_on();

	for (U8 i = 0; i < brightness; i++)
	{
		_delay(PULSE_DELAY_US);
	}

	led_off();

	for (U8 i = brightness; i < 255; i++)
	{
		_delay(PULSE_DELAY_US);
	}
}

void led_pulse(void)
{
	for (U8 brightness = 0; brightness < 255; brightness++)
	{
		pulse(brightness);
	}

	for (U8 brightness = 255; brightness > 0; brightness--)
	{
		pulse(brightness);
	}
}
