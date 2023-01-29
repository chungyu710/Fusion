#include "flex.h"

#include <xc.h>
#include <stddef.h>

#include "adc.h"
#include "system.h"

// Pin tristates
#define TRIS_THUMB    TRISA4
#define TRIS_INDEX    TRISC0
#define TRIS_MIDDLE   TRISC1
#define TRIS_RING     TRISC2
#define TRIS_PINKY    TRISC3

// ADC channels
#define ANSEL_THUMB   ANS3
#define ANSEL_INDEX   ANS4
#define ANSEL_MIDDLE  ANS5
#define ANSEL_RING    ANS6
#define ANSEL_PINKY   ANS7

// ADC_Channel enums
#define CHANNEL_THUMB   AN3
#define CHANNEL_INDEX   AN4
#define CHANNEL_MIDDLE  AN5
#define CHANNEL_RING    AN6
#define CHANNEL_PINKY   AN7

void flex_initialize(void)
{
	// Set pin tristates to inputs
	TRIS_THUMB = INPUT;
	TRIS_INDEX = INPUT;
	TRIS_MIDDLE = INPUT;
	TRIS_RING = INPUT;
	TRIS_PINKY = INPUT;

	// Enable analogue channels
	ANSEL_THUMB = ANALOGUE;
	ANSEL_INDEX = ANALOGUE;
	ANSEL_MIDDLE = ANALOGUE;
	ANSEL_RING = ANALOGUE;
	ANSEL_PINKY = ANALOGUE;
}

void flex_read(Flex * flex)
{
	if (flex == NULL)
	{
		system_abort(ABORT_NULL_POINTER);
	}

	flex->thumb = adc_read(CHANNEL_THUMB);
	flex->index = adc_read(CHANNEL_INDEX);
	flex->middle = adc_read(CHANNEL_MIDDLE);
	flex->ring = adc_read(CHANNEL_RING);
	flex->pinky = adc_read(CHANNEL_PINKY);
}
