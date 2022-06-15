#include <xc.h>
#include <pic16f690.h>

#include "system.h"

#include "tests/led.h"

void main(void)
{
	system_initialize();

	while (1)
	{
		test_led_blink();
	}
}
