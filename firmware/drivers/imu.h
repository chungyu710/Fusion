#ifndef IMU_H
#define IMU_H

#include "types.h"

void imu_initialize(void);
void imu_read(U8 address, void * data, U8 length);
void imu_write(U8 address, void * data, U8 length);
U8 imu_read_register(U8 address);
void imu_write_register(U8 address, U8 value);

#endif /* IMU_H */
