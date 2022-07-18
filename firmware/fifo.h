#ifndef FIFO_H
#define FIFO_H

#include <stdbool.h>

#include "types.h"

typedef struct FIFO FIFO;

struct FIFO
{
	U8 size;
	U8 * buffer;
	U8 length;
	U8 read;
	U8 write;
};

void fifo_initialize(FIFO * fifo, void * buffer, U8 size);
U8 fifo_read(FIFO * fifo);
void fifo_write(FIFO * fifo, U8 value);
bool fifo_is_empty(FIFO * fifo);
bool fifo_is_full(FIFO * fifo);

#endif /* FIFO_H */
