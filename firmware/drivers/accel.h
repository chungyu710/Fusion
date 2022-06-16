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

enum
{
	ACCEL_RANGE_2G,
	ACCEL_RANGE_4G,
	ACCEL_RANGE_8G,
	ACCEL_RANGE_16G,

	NUM_ACCEL_RANGES
};

void accel_initialize(void);
void accel_read(Accel * accel);
void accel_set_range(U8 range);
U8 accel_get_range(void);

#endif /* ACCEL_H */
