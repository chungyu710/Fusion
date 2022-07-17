#include <xc.h>
#include <stdio.h>

#include "system.h"

#include "imu.h"
#include "uart.h"
#include "led.h"

void main(void)
{
	system_initialize();

	while (1)
	{
		U8 request;
		led_on();
		uart_receive(&request, 1);
		led_off();
		system_service(request);
	}
}
