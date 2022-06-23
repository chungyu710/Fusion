#ifndef ACCEL_H
#define ACCEL_H

#include "types.h"
#include "system.h"

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
	// values for IMU CTRL1_XL register
	ACCEL_RANGE_2G = 0,
	ACCEL_RANGE_16G = 1,
	ACCEL_RANGE_4G = 2,
	ACCEL_RANGE_8G = 3,

	ACCEL_RANGE_UNKNOWN
};

void accel_initialize(void);
void accel_read(Accel * accel);
Status accel_set_range(Accel_Range range);

#endif /* ACCEL_H */
