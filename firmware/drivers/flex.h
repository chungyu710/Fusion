#ifndef FLEX_H
#define FLEX_H

#include "types.h"

struct Flex
{
	U8 thumb;
	U8 index;
	U8 middle;
	U8 ring;
	U8 pinky;
};

typedef struct Flex Flex;

void flex_initialize(void);
// functions to read flex sensors

#endif /* FLEX_H */
