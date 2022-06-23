#ifndef IMU_H
#define IMU_H

#include "types.h"

#define CTRL1_XL     0x10
#define CTRL2_G      0x11
#define CTRL3_C      0x12

#define STATUS_REG   0x1E

#define OUTX_L_A     0x28
#define OUTX_H_A     0x29

#define OUTX_L_G     0x22   // pitch

void imu_initialize(void);
void imu_read(U8 address, void * data, U8 length);
void imu_write(U8 address, void * data, U8 length);
U8 imu_read_register(U8 address);
void imu_write_register(U8 address, U8 value);

#endif /* IMU_H */
