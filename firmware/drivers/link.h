#ifndef LINK_H
#define LINK_H

#include "types.h"
#include "accel.h"
#include "gyro.h"
#include "flex.h"

enum Request
{
	REQUEST_ACCEL,
	REQUEST_GYRO,
	REQUEST_FLEX,
	REQUEST_SENSORS,
	REQUEST_BATTERY,

	NUM_REQUESTS
};

enum Result
{
	RESULT_SUCCESS,
	RESULT_ERROR,

	NUM_RESULTS
};

struct Sensors
{
	Accel accel;
	Gyro gyro;
	Flex flex;
};

struct Header
{
	U8 result;
	U8 length;
	U8 checksum;
	U8 sequence;
};

typedef enum Request Request;
typedef struct Sensors Sensors;

void link_initialize(void);
// other stuff here ....... like send and receive stuff

#endif /* LINK_H */
