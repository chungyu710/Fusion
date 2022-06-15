#ifndef GYRO_H
#define GYRO_H

#include "types.h"

struct Gyro
{
	U16 pitch;
	U16 yaw;
	U16 roll;
};

typedef struct Gyro Gyro;

void gyro_initialize(void);
// functions to read gyro and accel

#endif /* GYRO_H */
