#include <xc.h>
#include <pic16f690.h>

#include "system.h"
#include "led.h"

#include "tests/blink.h"

void main(void)
{
	system_initialize();
	led_initialize();

	while (1)
	{
		blink();
	}
}
