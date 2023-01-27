#include <xc.h>
#include <stdio.h>

#include "system.h"
#include "uart.h"
#include "led.h"
#include "battery.h"

void main(void)
{
	system_initialize();

	while (1)
	{
		// TODO: remove service from interrupt and use an RX buffer instead
		// TODO: check battery on a periodic timer
		if (battery_low())
		{
			led_pulse();
		}
	}
}

void __interrupt() isr()
{
	if (PIR1bits.RCIF)
	{
		U8 request;
		uart_receive(&request, 1);
		led_on();
		system_service(request);
		led_off();
	}
	else
	{
		system_abort();
	}
}
