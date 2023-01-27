#include "battery.h"

#include <xc.h>

#include "system.h"
#include "adc.h"

#define TRIS_BATTERY      TRISA2
#define ANSEL_BATTERY     ANS2
#define CHANNEL_BATTERY   AN2

#define LOW_BATTERY_mV   3600   // 3.6 V (HC-05 LDO minimum input voltage)
#define MAX_VOLTAGE_mV   5000   // 5 V (ADRES = 1023)

void battery_initialize(void)
{
	TRIS_BATTERY = INPUT;
	ANSEL_BATTERY = ANALOGUE;
}

U16 battery_voltage(void)
{
	/*
	The PCB contains a resistor divider that scales a 5 V
	suppy voltage down to a 3.3 V range.  The lithium-ion
	battery has a maximum voltage of 4.2 V and a typical
	voltage of 3.7 V.  However, the wired connection can
	be 5 V.  This means that an ADC reading of 1023
	corresponds to 5 V, so some post processing is required
	to convert this to a voltage in mV.
	*/

	U32 reading = adc_read(CHANNEL_BATTERY);
	return (U16)((reading * MAX_VOLTAGE_mV) / ADC_MAX);
}

bool battery_low(void)
{
	return battery_voltage() <= LOW_BATTERY_mV;
}
