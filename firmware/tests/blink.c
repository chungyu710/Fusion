#include "blink.h"

#include <xc.h>
#include <pic16f690.h>

#include "led.h"

void blink(void)
{
	_delay(3000000);

	while (1)
	{
		led_on();
		_delay(1000000);
		led_off();
		_delay(1000000);
	}
}
