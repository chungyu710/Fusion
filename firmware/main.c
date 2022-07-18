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
		led_on();
		while (fifo_is_empty(&rx_fifo));
		led_off();
		U8 request = fifo_read(&rx_fifo);

		//uart_receive(&request, 1);
		system_service(request);
		//uart_vomit();
		//_delay(100000);
	}
}
