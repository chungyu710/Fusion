#include <xc.h>
#include <stdio.h>

#include "system.h"
#include "uart.h"
#include "led.h"
#include "battery.h"

#define QUEUE_SIZE   5

static U8 queue [QUEUE_SIZE];
static int queue_read = 0;
static int queue_write = 0;
static int queue_length = 0;
static bool queue_overrun = false;

void main(void)
{
	system_initialize();

	while (1)
	{
		if (queue_length > 0)
		{
			U8 request = queue[queue_read];
			queue_read = (queue_read + 1) % QUEUE_SIZE;
			queue_length--;

			led_on();
			system_service(request);
			led_off();
		}

		if (queue_overrun)
		{
			system_abort();
		}

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
		if (queue_length < QUEUE_SIZE)
		{
			queue[queue_write] = RCREG;
			queue_write = (queue_write + 1) % QUEUE_SIZE;
			queue_length++;
		}
		else
		{
			queue_overrun = true;
		}
	}
}
