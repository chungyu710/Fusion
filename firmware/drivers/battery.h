#ifndef BATTERY_H
#define BATTERY_H

#include <stdbool.h>

#include "types.h"

void battery_initialize(void);
U16 battery_voltage(void);   // reported in mV
bool battery_low(void);
void battery_check(void);
bool battery_uvlo(void);   // undervolt lockout

#endif /* BATTERY_H */
