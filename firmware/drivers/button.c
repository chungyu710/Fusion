#include "button.h"

#include <xc.h>

#include "system.h"

#define TRIS_BUTTON   TRISC5
#define BUTTON        RC5

void button_initialize(void)
{
	TRIS_BUTTON = INPUT;
}

bool button_pressed(void)
{
	return BUTTON;
}

bool button_released(void)
{
	return !BUTTON;
}
