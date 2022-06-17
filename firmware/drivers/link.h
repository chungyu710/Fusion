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
typedef enum Sensor_Group Sensor_Group;

struct Sensors
{
	Accel accel;
	Gyro gyro;
	Flex flex;
};

enum Sensor_Group
{
	SENSOR_GROUP_ALL   = 0x0,
	SENSOR_GROUP_ACCEL = 0x1,
	SENSOR_GROUP_GYRO  = 0x2,
	SENSOR_GROUP_FLEX  = 0x3
};

enum Command
{
	COMMAND_PING        = 0x00,
	COMMAND_ACCEL_RANGE = 0x10,
	COMMAND_GYRO_RANGE  = 0x20,
	COMMAND_SENSORS     = 0x30,
	COMMAND_BATTERY     = 0x40,
	COMMAND_RESET       = 0x50
};

enum Status
{
	STATUS_SUCCESS         = 0x0,
	STATUS_ERROR           = 0x1,
	STATUS_UNKNOWN_REQUEST = 0x2,
	STATUS_LOW_BATTERY     = 0x3
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
