#ifndef LINK_H
#define LINK_H

#include "types.h"
#include "accel.h"
#include "gyro.h"
#include "flex.h"

typedef enum Request Request;
typedef enum Result Result;

typedef struct Response Response;
typedef struct Sensors Sensors;

enum Request
{
	REQUEST_ACCEL,
	REQUEST_GYRO,
	REQUEST_FLEX,
	REQUEST_SENSORS,
	REQUEST_BATTERY,

	NUM_REQUESTS
};

enum Status
{
	STATUS_SUCCESS,
	STATUS_ERROR,
	STATUS_LOW_BATTERY,
	STATUS_UNKNOWN_COMMAND,

	NUM_STATUS
};

struct Sensors
{
	Accel accel;
	Gyro gyro;
	Flex flex;
};

struct Response
{
	U8 status;
	U8 length;
	U8 checksum;
};

void link_initialize(void);
void link_respond(Result result, void * data, U8 length);

#endif /* LINK_H */
