#ifndef GYRO_H
#define GYRO_H

#include "types.h"

typedef struct Gyro Gyro;
typedef enum Gyro_Range Gyro_Range;

struct Gyro
{
	U16 pitch;
	U16 yaw;
	U16 roll;
};

enum Gyro_Range
{
	GYRO_RANGE_125_DPS,
	GYRO_RANGE_250_DPS,
	GYRO_RANGE_500_DPS,
	GYRO_RANGE_1000_DPS,
	GYRO_RANGE_2000_DPS,

	NUM_GYRO_RANGES
};

void gyro_initialize(void);
void gyro_read(Gyro * gyro);
void gyro_set_range(Gyro_Range range);

#endif /* GYRO_H */
