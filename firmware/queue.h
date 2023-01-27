#ifndef QUEUE_H
#define QUEUE_H

#include <stdbool.h>

#include "types.h"

typedef struct Queue Queue;

struct Queue
{
	U8 * data;
	U8 read;
	U8 write;
	U8 size;
	U8 length;
};

void queue_initialize(Queue * queue, U8 * data, U8 size);
bool queue_enqueue(Queue * queue, U8 value);
bool queue_dequeue(Queue * queue, U8 * value);
bool queue_empty(Queue * queue);
bool queue_full(Queue * queue);

#endif /* QUEUE_H */
