#include <xc.h>
#include <stdio.h>

#include "system.h"
#include "uart.h"
#include "led.h"
#include "battery.h"
#include "link.h"

#define BATTERY_POSTSCALER    100
#define UNDERVOLT_MAX_COUNT   5

static volatile U8 command;
static volatile bool pending_command = false;
static volatile bool check_battery = false;

void main(void)
{
	system_initialize();

	while (1)
	{
		if (pending_command)
		{
			led_on();
			system_service(command);
			pending_command = false;
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
				system_abort(ABORT_LOW_BATTERY, __func__);
			}

			check_battery = false;
		}
	}
}

void __interrupt() isr()
{
	if (PIR1bits.RCIF)
	{
		command = RCREG;   // Clears RCIF flag.
		pending_command = true;
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
