#include "led.h"

#include <xc.h>
#include <pic16f690.h>

#include "system.h"

#define LED        RC4
#define LED_TRIS   TRISC4

void led_initialize(void)
{
	LED_TRIS = OUTPUT;
}

void led_on(void)
{
	LED = 1;
}

void led_off(void)
{
	LED = 0;
}
