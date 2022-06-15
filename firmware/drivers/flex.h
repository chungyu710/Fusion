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
void flex_read(Flex * flex);

#endif /* FLEX_H */
