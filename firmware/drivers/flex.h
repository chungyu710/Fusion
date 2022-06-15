#ifndef FLEX_H
#define FLEX_H

#include "types.h"

typedef struct Flex Flex;

struct Flex
{
	U16 thumb;
	U16 index;
	U16 middle;
	U16 ring;
	U16 pinky;
};

void flex_initialize(void);
void flex_read(Flex * flex);

#endif /* FLEX_H */
