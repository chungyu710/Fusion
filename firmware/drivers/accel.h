#ifndef ACCEL_H
#define ACCEL_H

#include "types.h"

typedef struct Accel Accel;

struct Accel
{
	U16 x;
	U16 y;
	U16 z;
};

void accel_initialize(void);
void accel_read(Accel * accel);
// functions to read gyro and accel

#endif /* ACCEL_H */
