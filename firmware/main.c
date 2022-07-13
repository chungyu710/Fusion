#include <xc.h>
#include <stdio.h>

#include "system.h"

#include "imu.h"
#include "uart.h"
#include "led.h"

#include "tests/gyro.h"
#include "tests/accel.h"
#include "tests/led.h"

void main(void)
{
	system_initialize();
	//test_gyro();
	//test_accel();

	//printf("WHO_AM_I: 0x%02X\r\n", imu_read_register(WHO_AM_I));

	//test_led();

	while (1)
	{
		U8 request;
		led_on();
		uart_receive(&request, 1);
		led_off();
		system_service_sensors_only(request);
	}
}
