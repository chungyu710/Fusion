#ifndef IMU_H
#define IMU_H

#include "types.h"

void imu_initialize(void);
U8 imu_read(U8 address);
void imu_write(U8 address, U8 data);

#endif /* IMU_H */
