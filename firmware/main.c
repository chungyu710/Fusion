#include <xc.h>
#include <stdio.h>

#include "system.h"
#include "uart.h"
#include "led.h"
#include "battery.h"
#include "queue.h"

#define RX_BUFFER_SIZE       5
#define BATTERY_POSTSCALER   100

static Queue queue;
static volatile bool battery = false;

void main(void)
{
	// Initialize queue before system_initialize() enables interrupts.
	U8 rx_buffer [RX_BUFFER_SIZE];
	queue_initialize(&queue, rx_buffer, RX_BUFFER_SIZE);

	system_initialize();

	while (1)
	{
		U8 request;

		if (queue_dequeue(&queue, &request))
		{
			led_on();
			system_service(request);
			led_off();
		}

		if (battery)
		{
			if (battery_low())
			{
				system_low_battery();
			}

			battery = false;
		}
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
	else if (PIR1bits.TMR2IF)
	{
		// Check battery on first interrupt after boot.
		static volatile U8 postscaler = 0;

		postscaler++;    // increment prescaler

		if (postscaler == BATTERY_POSTSCALER)
		{
			postscaler = 0;
			battery = true;
		}

		PIR1bits.TMR2IF = 0;   // clear Timer2 interrupt flag
	}
}
