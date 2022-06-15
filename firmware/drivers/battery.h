#ifndef BATTERY_H
#define BATTERY_H

#include "types.h"

void battery_initialize(void);
U16 battery_voltage(void);   // reported in mV

// ADC reading is scaled to be 100% = 5 V, so some post processing is required to convert this to a voltage.

#endif /* BATTERY_H */
