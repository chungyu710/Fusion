#ifndef GYRO_H
#define GYRO_H

#include "types.h"
#include "system.h"

typedef struct Gyro Gyro;
typedef enum Gyro_Range Gyro_Range;

struct Gyro
{
	S16 pitch;
	S16 roll;
	S16 yaw;
} __attribute((packed));

enum Gyro_Range
{
	// values for IMU CTRL2_G register
	GYRO_RANGE_250_DPS = 0,
	GYRO_RANGE_500_DPS = 1,
	GYRO_RANGE_1000_DPS = 2,
	GYRO_RANGE_2000_DPS = 3,
	GYRO_RANGE_125_DPS = 5,   // dummy value (uses separate bit)

	GYRO_RANGE_UNKNOWN
};

void gyro_initialize(void);
void gyro_read(Gyro * gyro);
Status gyro_set_range(Gyro_Range range);

#endif /* GYRO_H */
