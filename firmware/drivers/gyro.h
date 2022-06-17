#ifndef GYRO_H
#define GYRO_H

#include "types.h"

typedef struct Gyro Gyro;

struct Gyro
{
	U16 pitch;
	U16 yaw;
	U16 roll;
};

enum
{
	GYRO_RANGE_125_DPS,
	GYRO_RANGE_250_DPS,
	GYRO_RANGE_500_DPS,
	GYRO_RANGE_1000_DPS,
	GYRO_RANGE_2000_DPS
};

void gyro_initialize(void);
void gyro_read(Gyro * gyro);
void gyro_set_range(U8 range);
U8 gyro_get_range(void);

#endif /* GYRO_H */
