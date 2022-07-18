#include "tests/button.h"

#include <xc.h>

#include "drivers/button.h"
#include "drivers/led.h"

void test_button(void)
{
	while (1)
	{
		if (button_pressed())
		{
			led_on();
		}
		else
		{
			led_off();
		}
	}
}
