#ifndef LINK_H
#define LINK_H

#include "types.h"
#include "accel.h"
#include "gyro.h"
#include "flex.h"

typedef enum Command Command;
typedef enum Status Status;
typedef struct Response Response;
typedef struct Sensors Sensors;

struct Sensors
{
	Accel accel;
	Gyro gyro;
	Flex flex;
};

enum
{
	SENSOR_GROUP_ALL,
	SENSOR_GROUP_ACCEL,
	SENSOR_GROUP_GYRO,
	SENSOR_GROUP_FLEX,

	NUM_SENSOR_GROUPS
};

enum Command
{
	COMMAND_PING,
	COMMAND_ACCEL,
	COMMAND_GYRO,
	COMMAND_SENSORS,
	COMMAND_BATTERY,

	NUM_COMMANDS
};

enum Status
{
	STATUS_SUCCESS,
	STATUS_ERROR,
	STATUS_LOW_BATTERY,
	STATUS_UNKNOWN_REQUEST,

	NUM_STATUSES
};

struct Response
{
	U8 status;
	U8 length;
	U8 checksum;
};

void link_initialize(void);
void link_respond(Status status, void * data, U8 length);

#endif /* LINK_H */
