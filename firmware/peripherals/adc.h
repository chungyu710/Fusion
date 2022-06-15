#ifndef ADC_H
#define ADC_H

#include "types.h"

void adc_initialize(void);
U16 adc_read(U8 channel);

#endif /* ADC_H */
