#ifndef LINK_H
#define LINK_H

#include "accel.h"
#include "gyro.h"
#include "flex.h"

enum Request
{
	REQUEST_SENSORS,
	REQUEST_BATTERY,

	NUM_REQUESTS
};

struct Sensors
{
	Accel accel;
	Gyro gyro;
	Flex flex;
};

typedef Request Request;
typedef Sensors Sensors;

void link_initialize(void);
// other stuff here ....... like send and receive stuff

#endif /* LINK_H */
