#ifndef FLEX_H
#define FLEX_H

#include "types.h"

struct Flex
{
	U16 thumb;
	U16 index;
	U16 middle;
	U16 ring;
	U16 pinky;
};

typedef struct Flex Flex;

void flex_initialize(void);
void flex_read(Flex * flex);

#endif /* FLEX_H */
