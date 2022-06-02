#include <xc.h>
#include <pic16f690.h>

#include "system.h"
#include "led.h"

void main(void)
{
	led_initialize();
	system_initialize();

	while (1)
	{

	}
}
