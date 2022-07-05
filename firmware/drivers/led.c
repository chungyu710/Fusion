#include "led.h"

#include <xc.h>

#include "system.h"

#define LED        RC4
#define TRIS_LED   TRISC4

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
