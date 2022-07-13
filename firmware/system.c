#include "system.h"

#include <xc.h>
#include <stddef.h>

#include "gpio.h"
#include "adc.h"
#include "led.h"
#include "uart.h"
#include "spi.h"
#include "imu.h"
#include "accel.h"
#include "gyro.h"
#include "link.h"
#include "battery.h"

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

void system_service_sensors_only(U8 request)
{
	Response response;
	Sensors sensors;
	void * payload;
	Command command = request & MASK_COMMAND;
	response.checksum = 3;

	if (command == COMMAND_SENSORS)
	{
		accel_read(&sensors.accel);
		gyro_read(&sensors.gyro);

		// dummy data until flex is working
		//flex_read(&sensors.flex);
		sensors.flex.thumb = 6;
		sensors.flex.index = 9;
		sensors.flex.middle = 4;
		sensors.flex.ring = 2;
		sensors.flex.pinky = 0;

		response.length = sizeof(Sensors);
		response.status = STATUS_SUCCESS;
		payload = &sensors;
	}
	else
	{
		response.status = STATUS_ERROR;
		response.length = 0;
		payload = NULL;
	}

	uart_transmit(&response, sizeof(Response));
	uart_transmit(payload, response.length);
}

static Status read_sensors(Sensor_Group group, void ** data, U8 * length)
{
	Sensors sensors;

	accel_read(&sensors.accel);
	gyro_read(&sensors.gyro);
	flex_read(&sensors.flex);

	Status status = STATUS_SUCCESS;

	switch (group)
	{
		default:
		{
			status = STATUS_ERROR;
			*data = NULL;
			*length = 0;
			break;
		}

		case SENSOR_GROUP_ALL:
		{
			*data = &sensors;
			*length = sizeof(sensors);
			break;
		}

		case SENSOR_GROUP_ACCEL:
		{
			*data = &sensors.accel;
			*length = sizeof(sensors.accel);
			break;
		}

		case SENSOR_GROUP_GYRO:
		{
			*data = &sensors.gyro;
			*length = sizeof(sensors.gyro);
			break;
		}

		case SENSOR_GROUP_FLEX:
		{
			*data = &sensors.flex;
			*length = sizeof(sensors.flex);
			break;
		}
	}

	return status;
}

void system_service(U8 request)
{
	Command command = request & MASK_COMMAND;
	U8 metadata = request & MASK_METADATA;

	switch (command)
	{
		default:
		{
			link_respond(STATUS_ERROR, NULL, 0);
			break;
		}

		case COMMAND_PING:
		{
			link_respond(STATUS_SUCCESS, NULL, 0);
			break;
		}

		case COMMAND_ACCEL_RANGE:
		{
			Status status = accel_set_range(metadata);
			link_respond(status, NULL, 0);
			break;
		}

		case COMMAND_GYRO_RANGE:
		{
			Status status = gyro_set_range(metadata);
			link_respond(status, NULL, 0);
			break;
		}

		case COMMAND_SENSORS:
		{
			void * data;
			U8 length;
			Status status = read_sensors(metadata, &data, &length);
			link_respond(status, data, length);
			break;
		}

		case COMMAND_BATTERY:
		{
			U16 voltage = battery_voltage();
			link_respond(STATUS_SUCCESS, &voltage, sizeof(voltage));
			break;
		}

		case COMMAND_RESET:
		{
			// reset here?  then send response?  or send response  first  then reset?
			link_respond(STATUS_ERROR, NULL, 0);
			break;
		}
	}
}
