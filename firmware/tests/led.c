#include "tests/led.h"

#include <xc.h>

#include "drivers/led.h"

#define SECOND_US   1000000

void test_led(void)
{
	while (1)
	{
		led_blink();
	}
}
