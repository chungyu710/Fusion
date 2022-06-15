#include "adc.h"

#include <xc.h>
#include <pic16f690.h>

void adc_initialize(void)
{
	// ANALOGUE (1) / DIGITAL (0) //

	/*
	====================================================================
	| Register |                  ADC Channel                          |
	|----------|-------------------------------------------------------|
	| ANSEL    |  AN7 |  AN6 |  AN5 |  AN4 |  AN3 |  AN2 |  AN1 |  AN0 |
	| ANSELH   |    X |    X |    X |    X | AN11 | AN10 |  AN9 |  AN8 |
	====================================================================
	*/

	// disable all ADC channels
	ANSEL  = 0b00000000;
	ANSELH = 0b00000000;
}
