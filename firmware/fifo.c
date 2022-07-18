#include "fifo.h"

void fifo_initialize(FIFO * fifo, void * buffer, U8 size)
{
	fifo->size = size;
	fifo->buffer = buffer;
	fifo->length = 0;
	fifo->read = 0;
	fifo->write = 0;
}

U8 fifo_read(FIFO * fifo)
{
	if (fifo_is_empty(fifo))
	{
		return 0xFF;
	}

	U8 value = fifo->buffer[fifo->read];
	fifo->read = (fifo->read + 1) % fifo->size;
	fifo->length--;
	return value;
}

void fifo_write(FIFO * fifo, U8 value)
{
	if (fifo_is_full(fifo))
	{
		return;
	}

	fifo->buffer[fifo->write] = value;
	fifo->write = (fifo->write + 1) % fifo->size;
	fifo->length++;
}

bool fifo_is_empty(FIFO * fifo)
{
	return fifo->length == 0;
}

bool fifo_is_full(FIFO * fifo)
{
	return fifo->length == fifo->size;
}

//void fifo_print(FIFO * fifo)
//{
//	U8 index = fifo->read;
//	printf("size %u, length %u, read %u, write %u\r\n", fifo->size, fifo->length, fifo->read, fifo->write);

//	for (U8 i = 0; i < fifo->length; i++)
//	{
//		printf("%u ", fifo->buffer[index]);
//		index = (index + 1) % fifo->size;
//	}

//	printf("\r\n");
//}

//int main(void)
//{
//	FIFO fifo;
//	char buffer [5];
//	fifo_initialize(&fifo, &buffer, sizeof(buffer));
//	fifo_print(&fifo);
//	fifo_write(&fifo, 1);
//	fifo_print(&fifo);
//	fifo_write(&fifo, 2);
//	fifo_write(&fifo, 3);
//	fifo_write(&fifo, 4);
//	fifo_print(&fifo);
//	fifo_write(&fifo, 5);
//	fifo_write(&fifo, 6);
//	fifo_print(&fifo);
//	printf("read %u\n", fifo_read(&fifo));
//	fifo_print(&fifo);
//	fifo_write(&fifo, 6);
//	fifo_print(&fifo);
//	printf("read %u\n", fifo_read(&fifo));
//	fifo_print(&fifo);
//	printf("read %u\n", fifo_read(&fifo));
//	fifo_print(&fifo);
//	printf("read %u\n", fifo_read(&fifo));
//	fifo_print(&fifo);
//	printf("read %u\n", fifo_read(&fifo));
//	fifo_print(&fifo);
//	printf("read %u\n", fifo_read(&fifo));
//	fifo_print(&fifo);
//	printf("read %u\n", fifo_read(&fifo));
//	fifo_print(&fifo);
//	fifo_write(&fifo, 7);
//	fifo_write(&fifo, 8);
//	fifo_print(&fifo);
//	return 0;
//}
