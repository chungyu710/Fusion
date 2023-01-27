#include "queue.h"

void queue_initialize(Queue * queue, U8 * data, U8 size)
{
	queue->data = data;
	queue->size = size;
	queue->length = 0;
	queue->read = 0;
	queue->write = 0;
}

bool queue_enqueue(Queue * queue, U8 value)
{
	if (queue_full(queue))
	{
		return false;
	}

	queue->data[queue->write] = value;
	queue->write = (queue->write + 1) % queue->size;
	queue->length++;
	return true;
}

bool queue_dequeue(Queue * queue, U8 * value)
{
	if (queue_empty(queue))
	{
		return false;
	}

	*value = queue->data[queue->read];
	queue->read = (queue->read + 1) % queue->size;
	queue->length--;
	return true;
}

bool queue_empty(Queue * queue)
{
	return queue->length == 0;
}

bool queue_full(Queue * queue)
{
	return queue->length == queue->size;
}
