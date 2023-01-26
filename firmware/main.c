#include <xc.h>
#include <stdio.h>

#include "system.h"
#include "uart.h"
#include "led.h"
#include "battery.h"
#include "queue.h"

#define RX_BUFFER_SIZE   5

static Queue queue;
//static bool initialized = false;

void main(void)
{
	// Initialize queue before system_initialize() enables interrupts.
	U8 rx_buffer [RX_BUFFER_SIZE];
	queue_initialize(&queue, rx_buffer, RX_BUFFER_SIZE);

	system_initialize();

	//initialized = true;

	while (1)
	{
		U8 request;

		if (queue_dequeue(&queue, &request))
		{
			led_on();
			system_service(request);
			led_off();
		}

		// TODO: check battery on a periodic timer
		//if (battery_low())
		//{
		//	led_pulse();
		//}
	}
}

void __interrupt() isr()
{
	if (PIR1bits.RCIF)
	{
		if (!queue_enqueue(&queue, RCREG))
		{
			system_abort(ABORT_RX_QUEUE_FULL);
		}
	}
}
