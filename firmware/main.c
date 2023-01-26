#include <xc.h>
#include <stdio.h>

#include "system.h"
#include "uart.h"
#include "led.h"
#include "battery.h"
#include "queue.h"

#define RX_BUFFER_SIZE          5
#define BATTERY_POSTSCALER      100
#define UNDERVOLT_MAX_COUNT   5

static Queue queue;
static volatile bool check_battery = false;

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

		if (check_battery)
		{
			static U8 count = 0;

			if (battery_low())
			{
				count++;
			}

			if (count == UNDERVOLT_MAX_COUNT)
			{
				count = 0;
				system_abort(ABORT_LOW_BATTERY);
			}

			check_battery = false;
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
			check_battery = true;
		}

		PIR1bits.TMR2IF = 0;   // clear Timer2 interrupt flag
	}
}
