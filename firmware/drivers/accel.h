#ifndef ACCEL_H
#define ACCEL_H

#include "types.h"

typedef struct Accel Accel;
typedef struct Accel_Range Accel_Range;

struct Accel
{
	U16 x;
	U16 y;
	U16 z;
};

enum Accel_Range
{
	ACCEL_RANGE_2G,
	ACCEL_RANGE_4G,
	ACCEL_RANGE_8G,
	ACCEL_RANGE_16G
};

void accel_initialize(void);
void accel_read(Accel * accel);
void accel_set_range(Accel_Range range);

#endif /* ACCEL_H */
