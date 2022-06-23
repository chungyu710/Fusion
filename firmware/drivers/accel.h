#ifndef ACCEL_H
#define ACCEL_H

#include "types.h"

typedef struct Accel Accel;
typedef enum Accel_Range Accel_Range;

struct Accel
{
	S16 x;
	S16 y;
	S16 z;
};

enum Accel_Range
{
	ACCEL_RANGE_2G,
	ACCEL_RANGE_4G,
	ACCEL_RANGE_8G,
	ACCEL_RANGE_16G,

	NUM_ACCEL_RANGES
};

void accel_initialize(void);
void accel_read(Accel * accel);
void accel_set_range(Accel_Range range);

#endif /* ACCEL_H */
