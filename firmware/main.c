#include <xc.h>
#include <stdio.h>

#include "system.h"
#include "uart.h"
#include "led.h"

#include"tests/button.h"

void main(void)
{
	system_initialize();

	while (1)
	{
		test_button();
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
