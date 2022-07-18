#include "battery.h"

#include <xc.h>

#include "system.h"

#define TRIS_BATTERY    TRISA2
#define ANSEL_BATTERY   ANS2

#define LOW_BATTERY_mV   3300   // 3.3 V

void battery_initialize(void)
{

}

U16 battery_voltage(void)
{
	return 69;   // change this later
}

bool battery_low(void)
{
	return battery_voltage() <= LOW_BATTERY_mV;
}
