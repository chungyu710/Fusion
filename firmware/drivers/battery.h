#ifndef BATTERY_H
#define BATTERY_H

#include "types.h"

void battery_initialize(void);
U16 battery_voltage(void);   // reported in mV

#endif /* BATTERY_H */
