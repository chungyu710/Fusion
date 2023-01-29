#include "battery.h"

#include <xc.h>

#include "system.h"
#include "adc.h"

#define TRIS_BATTERY      TRISA2
#define ANSEL_BATTERY     ANS2
#define CHANNEL_BATTERY   AN2

/*
The HC-05 bluetooth module is directly
powered from the battery since it has
its own LDO.  The minimim input voltage
is 3.6 V, so if the battery drops below
this voltage, Fusion cannot operate reliably.
*/

#define LOW_BATTERY_mV   3600   // 3.6 V (HC-05 LDO minimum input voltage)
#define MAX_VOLTAGE_mV   5000   // 5 V (ADRES = 1023)

#define BOOT_DELAY_US   10000   // 10 ms

void battery_initialize(void)
{
	TRIS_BATTERY = INPUT;
	ANSEL_BATTERY = ANALOGUE;

	// TIMER 2 //

	/*
	The Timer2 value is saved in TMR2.  It takes
	(Fosc / 4) / prescaler as input and compares
	TMR2 to PR2.  TMR2 always resets to 0 and
	increments until it matches PR2.  After every
	match the postscaler counter is incremented.
	When the postscaler overflows the PIR1.TMR2IF
	interrupt flag is set and must be cleared manually.
	The prescaler and postscaler effectively slow down
	reduce the frequency of the timer.
	*/

	// Use maximum prescaler settings for slowest interval.
	T2CONbits.TMR2ON = 1;        // turn on timer
	T2CONbits.T2CKPS = 0b11;     // 1:16 prescaler
	T2CONbits.TOUTPS = 0b1111;   // 1:16 postscaler

	PIE1bits.TMR2IE = 1;         // enable Timer2 interrupt

	PR2 = 255;   // set timer period (interrupt frequency = Fosc / 4 / prescaler / PR2 / postscaler)
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
