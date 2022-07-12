#ifndef SYSTEM_H
#define SYSTEM_H

#define OUTPUT   0
#define INPUT    1

#define DIGITAL    0
#define ANALOGUE   1

#include "types.h"

typedef enum Status Status;

enum Status
{
	STATUS_SUCCESS         = 0x0,
	STATUS_ERROR           = 0x1,
	STATUS_UNKNOWN_REQUEST = 0x2,
	STATUS_LOW_BATTERY     = 0x3
};

void system_initialize(void);
void system_service(U8 request);

#endif /* SYSTEM_H */
