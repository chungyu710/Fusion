#include <xc.h>

#include "system.h"
#include "battery.h"
#include "link.h"

#define BATTERY_CHECK_POSTSCALER    100

static volatile U8 data = 0;
static volatile bool request = false;
static volatile bool battery = false;

void main(void)
{
	system_initialize();

	while (1)
	{
		if (request)
		{
			link_service(data);
			request = false;
		}

		if (battery)
		{
			battery_check();
			battery = false;
		}
	}
}

void __interrupt() isr()
{
	if (PIR1bits.RCIF)
	{
		data = RCREG;   // Clears RCIF flag.
		request = true;
	}
	else if (PIR1bits.TMR2IF)
	{
		// Check battery on first interrupt after boot.
		static volatile U8 postscaler = 0;

		postscaler++;    // increment prescaler

		if (postscaler == BATTERY_CHECK_POSTSCALER)
		{
			postscaler = 0;
			battery = true;
		}

		PIR1bits.TMR2IF = 0;   // clear Timer2 interrupt flag
	}
}
