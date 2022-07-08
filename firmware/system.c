#include "system.h"

#include <xc.h>

#include "gpio.h"
#include "adc.h"
#include "led.h"
#include "uart.h"
#include "spi.h"
#include "imu.h"
#include "accel.h"
#include "gyro.h"
#include "link.h"

// ======= CONFIGURATION BITS ======= //

#pragma config FOSC = INTRCIO   // use internal oscillotor and use clock pins as GPIO
#pragma config WDTE = OFF       // disable watchdog timer
#pragma config PWRTE = OFF      // disable powerup timer
#pragma config MCLRE = OFF      // set MCLR pin as digital input (disable reset functionality)
#pragma config CP = OFF         // disable program memory protection
#pragma config CPD = OFF        // disable data memory protection
#pragma config BOREN = ON       // enable brownout reset (ensures that power-on reset works properly)
#pragma config IESO = OFF       // disable internal-external switchover
#pragma config FCMEN = OFF      // disable failsafe clock monitor

// ================================== //

#define LED_DELAY    200000
#define LED_BLINKS   3

void system_initialize(void)
{
	// OSCILLATOR //

	OSCCONbits.IRCF = 0b111;      // set clock frequency to 8 MHz
	OSCCONbits.SCS = 1;           // use internal oscillator as system clock
	OSCTUNEbits.TUN = 0b00000;    // use factory-calibrated frequency

	// PERIPHERALS //

	gpio_initialize();
	adc_initialize();
	spi_initialize();
	uart_initialize();

	// DRIVERS //

	led_initialize();
	imu_initialize();
	accel_initialize();
	gyro_initialize();

	// STARTUP INDICATOR //

	for (int i = 0; i < LED_BLINKS; i++)
	{
		led_on();
		_delay(LED_DELAY);
		led_off();
		_delay(LED_DELAY);
	}
}

//void system_service(U8 request)
//{
//	Command command = request & 0xF0;
//	U8 metadata = request & 0x0F;
//	Status status;
//	void * data;
//	U8 length;

//	switch (command)
//	{
//		case COMMAND_PING:
//		{
//			status = STATUS_SUCCESS;
//			data = NULL;
//			length = 0;
//		}

//		case COMMAND_ACCEL_RANGE:
//		{
//			Accel_Range range = metadata;
//			Status status = accel_set_range(range);
//			break;
//		}

//		case COMMAND_GYRO_RANGE:
//		{
//			Gyro_Range range = metadata;
//			Status status = gyro_set_range(range);
//			break;
//		}

//		case COMMAND_SENSORS:
//		{
//			Sensors sensors;

//			accel_read(&sensors.accel);
//			gyro_read(&sensors.gyro);
//			flex_read(&sensors.flex);

//			Sensor_Group group = metadata;

//			switch (group)
//			{
//				case SENSOR_GROUP_ALL:
//				{
//					status = STATUS_SUCCESS;
//					data = &sensors;
//					length = sizeof(Sensors);
//					break;
//				}

//				case SENSOR_GROUP_ACCEL:
//				{
//					status = STATUS_SUCCESS;
//					data = &sensors.accel;
//					length = sizeof(Accel);
//					break;
//				}

//				case SENSOR_GROUP_GYRO:
//				{
//					status = STATUS_SUCCESS;
//					data = &sensors.gyro;
//					length = sizeof(Gyro);
//					break;
//				}

//				case SENSOR_GROUP_FLEX:
//				{
//					status = STATUS_SUCCESS;
//					data = &sensors.flex;
//					length = sizeof(Flex);
//					break;
//				}

//				default:
//				{
//					status = STATUS_ERROR;
//					data = NULL;
//					length = 0;
//				}
//			}

//			break;
//		}

//		case COMMAND_BATTERY:
//			break;
//		case COMMAND_RESET:
//			break;

//		default:
//			break;
//	}

//	link_respond(status, data, length);
//}
