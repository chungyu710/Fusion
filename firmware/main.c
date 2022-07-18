#include <xc.h>
#include <stdio.h>
#include <stdbool.h>

#include "system.h"

#include "imu.h"
#include "uart.h"
#include "led.h"

void main(void)
{
	system_initialize();

	while (1)
	{

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
}
