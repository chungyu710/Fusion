#ifndef ADC_H
#define ADC_H

#include "types.h"

void adc_initialize(void);
U16 adc_read(unsigned int channel);

#endif /* ADC_H */
