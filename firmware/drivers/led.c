#include "led.h"

#include <xc.h>

#include "system.h"

#define LED        RC4
#define TRIS_LED   TRISC4

#define LED_BLINK_DELAY_US   500000

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
	_delay(LED_BLINK_DELAY_US);
	led_off();
	_delay(LED_BLINK_DELAY_US);
}

void led_blink_forever(void)
{
	while (1)
	{
		led_blink();
	}
}
