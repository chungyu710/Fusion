#include "system.h"

#include <xc.h>
#include <stddef.h>
#include <string.h>

#include "gpio.h"
#include "adc.h"
#include "led.h"
#include "uart.h"
#include "spi.h"
#include "imu.h"
#include "accel.h"
#include "gyro.h"
#include "link.h"
#include "button.h"
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

#define LED_DELAY_US   200000
#define LED_BLINKS     3

static bool system_streaming = false;

static char * system_abort_reasons [ABORT_count] = {
	"NULL POINTER",
	"IMU OFFLINE",
	"LOW BATTERY",
	"QUEUE FULL",
};

void system_initialize(void)
{
	// OSCILLATOR //

	OSCCONbits.IRCF = 0b111;      // set clock frequency to 8 MHz
	OSCCONbits.SCS = 1;           // use internal oscillator as system clock
	OSCTUNEbits.TUN = 0b00000;    // use factory-calibrated frequency

	// INTERRUPTS //

	INTCONbits.PEIE = 1;   // enable peripherial interrupts

	// WATCHDOG //

	WDTCONbits.SWDTEN = 0;    // disable watchdog timer to prevent reset
	OPTION_REGbits.PSA = 1;   // assign prescaler to watchdog timer instead of Timer 0
	WDTCONbits.WDTPS = 0;     // set watchdog prescaler to fasest setting

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
	flex_initialize();
	button_initialize();
	battery_initialize();

	// STARTUP INDICATOR //

	for (int i = 0; i < LED_BLINKS; i++)
	{
		led_on();
		_delay(LED_DELAY_US);
		led_off();
		_delay(LED_DELAY_US);
	}

	// ENABLE ALL INTERRUPTS //

	INTCONbits.GIE = 1;
}

void system_abort(Abort abort, char const * message)
{
	while (button_released())
	{
		if (abort == ABORT_LOW_BATTERY)
		{
			led_pulse();   // Fade LED in and out during low battery.
		}
		else
		{
			led_blink();   // Blink LED during firmware errors.
		}

		if (abort < ABORT_count)
		{
			char * reason = system_abort_reasons[abort];
			char * newline = "\r\n";

			uart_transmit(reason, strlen(reason));

			if (message != NULL)
			{
				char * colon = " : ";
				uart_transmit(colon, strlen(colon));
				uart_transmit(message, strlen(message));
			}

			uart_transmit(newline, strlen(newline));
		}
	}

	system_reboot();
}

void system_fatal(void)
{
	while (1)
	{
		led_blink_slow();
	}
}

static Status read_sensors(Sensor_Group group, void ** data, U8 * length)
{
	Sensors sensors;

	accel_read(&sensors.accel);
	gyro_read(&sensors.gyro);
	flex_read(&sensors.flex);
	sensors.button = button_pressed();

	Status status = STATUS_SUCCESS;

	switch (group)
	{
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
		case SENSOR_GROUP_BUTTON:
		{
			*data = &sensors.button;
			*length = sizeof(sensors.button);
			break;
		}
		default:
		{
			status = STATUS_ERROR;
			*data = NULL;
			*length = 0;
			break;
		}
	}

	return status;
}

static Status stream_update(Stream_Command command)
{
	Status status = STATUS_SUCCESS;

	switch (command)
	{
		case STREAM_START:
		{
			system_streaming = true;
			break;
		}
		case STREAM_STOP:
		{
			system_streaming = false;
			break;
		}
		default:
		{
			status = STATUS_ERROR;
			break;
		}
	}

	return status;
}

void system_service(U8 request)
{
	led_on();

	Command command = request & COMMAND_MASK;
	U8 meta = request & METADATA_MASK;

	switch (command)
	{
		case COMMAND_PING:
		{
			link_respond(STATUS_SUCCESS, NULL, 0);
			break;
		}
		case COMMAND_ACCEL_RANGE:
		{
			Status status = accel_set_range(meta);
			link_respond(status, NULL, 0);
			break;
		}
		case COMMAND_GYRO_RANGE:
		{
			Status status = gyro_set_range(meta);
			link_respond(status, NULL, 0);
			break;
		}
		case COMMAND_SAMPLE:
		{
			void * data;
			U8 length;
			Status status = read_sensors(meta, &data, &length);
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
			link_respond(STATUS_SUCCESS, NULL, 0);
			system_reboot();
			break;
		}
		case COMMAND_STREAM:
		{
			Status status = stream_update(meta);
			link_respond(status, NULL, 0);
			break;
		}
		default:
		{
			link_respond(STATUS_ERROR, NULL, 0);
			break;
		}
	}

	led_off();
}

void system_reboot(void)
{
	WDTCONbits.SWDTEN = 1;   // enable watchdog timer to force reset
}

#include <stdio.h>
void system_streaming_service(void)
{
	if (system_streaming)
	{
		system_service(COMMAND_SAMPLE);
		//printf("STREAM\r\n");
	}
	else
	{
		//printf("STOP\r\n");
	}
}
