#include "accel.h"

#include <xc.h>
#include <pic16f690.h>

#include "imu.h"

void accel_initialize(void)
{
	imu_write_register(CTRL1_XL, 0x40);   // enable
}

void accel_read(Accel * accel);
void accel_set_range(Accel_Range range);
