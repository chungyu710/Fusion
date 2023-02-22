#include "link.h"

#include <xc.h>
#include <stddef.h>

#include "uart.h"
#include "battery.h"
#include "button.h"
#include "accel.h"
#include "gyro.h"
#include "flex.h"

void link_respond(Status status, void * payload, U8 size)
{
	Header header;
	header.status = status;
	header.size = size;
	header.checksum = header.status ^ header.size;

	if (payload != NULL)
	{
		char * bytes = (char *)payload;

		for (U8 i = 0; i < size; i++)
		{
			header.checksum ^= bytes[i];
		}
	}

	uart_transmit(&header, sizeof(Header));

	if (payload != NULL)
	{
		uart_transmit(payload, size);
	}
}

static Status read_sensors(Sensor_Group group, void * data, U8 * length)
{
	Status status = STATUS_SUCCESS;

	switch (group)
	{
		case SENSOR_GROUP_ALL:
		{
			Sensors * sensors = data;
			accel_read(&sensors->accel);
			flex_read(&sensors->flex);
			gyro_read(&sensors->gyro);
			sensors->button = button_pressed();
			*length = sizeof(Sensors);
			break;
		}
		case SENSOR_GROUP_ACCEL:
		{
			Accel * accel = data;
			accel_read(accel);
			*length = sizeof(Accel);
			break;
		}
		case SENSOR_GROUP_GYRO:
		{
			Gyro * gyro = data;
			gyro_read(gyro);
			*length = sizeof(Gyro);
			break;
		}
		case SENSOR_GROUP_FLEX:
		{
			Flex * flex = data;
			flex_read(flex);
			*length = sizeof(Flex);
			break;
		}
		case SENSOR_GROUP_BUTTON:
		{
			U8 * button = data;
			*button = button_pressed();
			*length = sizeof(U8);
			break;
		}
		default:
		{
			status = STATUS_ERROR;
			*length = 0;
			break;
		}
	}

	return status;
}

void link_service(U8 request)
{
	Command command = request & COMMAND_MASK;
	U8 meta = request & METADATA_MASK;
	Status status = STATUS_SUCCESS;

	if (battery_uvlo())
	{
		status = STATUS_LOW_BATTERY;
		command = COMMAND_BATTERY;
	}

	switch (command)
	{
		case COMMAND_PING:
		{
			link_respond(status, NULL, 0);
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
		case COMMAND_BURST:
		{
			U8 burst = BURST_SIZE;

			if (command == COMMAND_SAMPLE)
			{
				burst = 1;
			}

			for (U8 i = 0; i < burst; i++)
			{
				U8 data [sizeof(Sensors)];   // big enough to hold all sensor groups
				U8 length;
				Status status = read_sensors(meta, &data, &length);
				link_respond(status, data, length);
			}

			break;
		}
		case COMMAND_BATTERY:
		{
			U16 voltage = battery_voltage();
			link_respond(status, &voltage, sizeof(voltage));
			break;
		}
		case COMMAND_RESET:
		{
			link_respond(status, NULL, 0);
			system_reboot();
			break;
		}
		default:
		{
			link_respond(STATUS_ERROR, NULL, 0);
			break;
		}
	}
}
