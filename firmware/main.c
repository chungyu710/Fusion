#include <xc.h>

#include "system.h"
#include "uart.h"
#include "led.h"
#include "battery.h"
#include "link.h"

#define BATTERY_POSTSCALER    100
#define UNDERVOLT_MAX_COUNT   5

// RX QUEUE //

//struct Queue
//{
//	U8 read;
//	U8 write;
//	U8 length;
//	U8 size;
//	U8 data [10];
//};

//typedef struct Queue Queue;

//static volatile Queue queue;
static volatile bool queue_full = false;
static volatile bool pending_request = false;
static volatile bool check_battery = false;
static volatile U8 request = 0;

void main(void)
{
	system_initialize();

	//queue.read = 0;
	//queue.write = 0;
	//queue.length = 0;
	//queue.size = sizeof(queue.data);

	while (1)
	{
		if (pending_request)
		{
			//U8 request = queue.data[queue.read];
			//queue.read = (queue.read + 1) % queue.size;
			//queue.length--;
			system_service(request);
			pending_request = false;
		}

		if (queue_full)
		{
			ABORT(ABORT_QUEUE_FULL);
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
				ABORT(ABORT_LOW_BATTERY);
			}

			check_battery = false;
		}

		//system_streaming_service();
	}
}

void __interrupt() isr()
{
	if (PIR1bits.RCIF)
	{
		//if (queue.length == queue.size)
		//{
		//	queue_full = true;
		//}
		//else
		//{
			//queue.data[queue.write] = RCREG;   // Clears RCIF flag.
			//queue.write = (queue.write + 1) % queue.size;
			//queue.length++;
			request = RCREG;   // Clears RCIF flag.
			pending_request = true;
		//}
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
