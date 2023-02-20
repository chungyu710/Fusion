#include "link.h"

#include <xc.h>
#include <stddef.h>

#include "uart.h"

void link_respond(Status status, void * payload, U8 size)
{
	Header header;
	header.status = status;
	header.size = size;
	header.checksum = header.status ^ header.size;

	if (payload != NULL)
	{
		char * bytes = (char *)payload;

		for (U8 i = 0; i < size; i++)
		{
			header.checksum ^= bytes[i];
		}
	}

	uart_transmit(&header, sizeof(Header));

	if (payload != NULL)
	{
		uart_transmit(payload, size);
	}
}
