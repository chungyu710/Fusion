#ifndef ADC_H
#define ADC_H

#include "types.h"

#include <stdbool.h>

#define ADC_MIN   0
#define ADC_MAX   1023

#define TRIS_AN0    TRISA0
#define TRIS_AN1    TRISA1
#define TRIS_AN2    TRISA2
#define TRIS_AN3    TRISA4
#define TRIS_AN4    TRISC0
#define TRIS_AN5    TRISC1
#define TRIS_AN6    TRISC2
#define TRIS_AN7    TRISC3
#define TRIS_AN8    TRISC6
#define TRIS_AN9    TRISC7
#define TRIS_AN10   TRISB4
#define TRIS_AN11   TRISB5

typedef enum ADC_Channel ADC_Channel;

enum ADC_Channel
{
	AN0,
	AN1,
	AN2,
	AN3,
	AN4,
	AN5,
	AN6,
	AN7,
	AN8,
	AN9,
	AN10,
	AN11
};

void adc_initialize(void);
U16 adc_read(ADC_Channel channel);

#endif /* ADC_H */
