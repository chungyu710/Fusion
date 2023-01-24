#include "adc.h"

#include <xc.h>

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

	ADCON0bits.ADFM    = 1;   // right justify result
	ADCON0bits.VCFG    = 0;	  // use power supply voltage as reference voltage
	ADCON0bits.CHS     = 0;   // reset channel to AN0
	ADCON0bits.GO_DONE = 0;   // don't run ADC conversion
	ADCON0bits.ADON    = 1;   // enable ADC
}

U16 adc_read(ADC_Channel channel)
{
	ADCON0bits.CHS = channel;
	ADCON0bits.GO_DONE = 1;                    // set the GO/DONE bit
	while(ADCON0bits.GO_DONE == 1) {}          // monitor GO/DONE bit until it clears
	return ((U16)ADRESH << 8) | (U16)ADRESL;   // read ADRESH bits
}
