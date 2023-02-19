#ifndef LINK_H
#define LINK_H

#include "types.h"
#include "accel.h"
#include "gyro.h"
#include "flex.h"
#include "system.h"

#define MASK_COMMAND    0xF0
#define MASK_METADATA   0x0F

typedef enum Command Command;
typedef enum Sensor_Group Sensor_Group;
typedef enum Stream_Command Stream_Command;

typedef struct Header Header;
typedef struct Sensors Sensors;

enum Sensor_Group
{
	SENSOR_GROUP_ALL     = 0x0,
	SENSOR_GROUP_ACCEL   = 0x1,
	SENSOR_GROUP_GYRO    = 0x2,
	SENSOR_GROUP_FLEX    = 0x3,
	SENSOR_GROUP_BUTTON  = 0x4
};

enum Stream_Command
{
	STREAM_START  = 0x0,
	STREAM_STOP   = 0x1
};

enum Command
{
	COMMAND_PING        = 0x00,
	COMMAND_ACCEL_RANGE = 0x10,
	COMMAND_GYRO_RANGE  = 0x20,
	COMMAND_SAMPLE      = 0x30,
	COMMAND_BATTERY     = 0x40,
	COMMAND_RESET       = 0x50,
	COMMAND_STREAM      = 0x60,
};

struct Sensors
{
	Accel accel;
	Gyro gyro;
	Flex flex;
	U8 button;
} __attribute((packed));

struct Header
{
	U8 status;
	U8 size;
	U8 checksum;
} __attribute((packed));

void link_respond(Status status, void * data, U8 size);

#endif /* LINK_H */
