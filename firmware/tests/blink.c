#include "blink.h"

#include <xc.h>
#include <pic16f690.h>

#include "led.h"

#define SECOND_US   1000000

void blink(void)
{
	_delay(3 * SECOND_US);

	while (1)
	{
		led_on();
		_delay(SECOND_US);
		led_off();
		_delay(SECOND_US);
	}
}
