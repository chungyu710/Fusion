#ifndef SYSTEM_H
#define SYSTEM_H

#define OUTPUT   0
#define INPUT    1

#define DIGITAL    0
#define ANALOGUE   1

#define ABORT(reason)   system_abort(reason, __func__)

#include "types.h"

typedef enum Status Status;
typedef enum Abort Abort;

enum Status
{
	STATUS_SUCCESS     = 0x0,
	STATUS_ERROR       = 0x1,
	STATUS_LOW_BATTERY = 0x2
};

enum Abort
{
	ABORT_NULL_POINTER,
	ABORT_IMU_OFFLINE,
	ABORT_LOW_BATTERY,
	ABORT_QUEUE_FULL,

	ABORT_count
};

void system_initialize(void);
void system_abort(Abort reason, char const * message);
void system_fatal(void);
void system_service(U8 request);
void system_reboot(void);
void system_streaming_service(void);

#endif /* SYSTEM_H */
