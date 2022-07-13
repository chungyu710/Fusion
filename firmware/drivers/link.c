#include "link.h"

#include <xc.h>

#include "uart.h"

void link_respond(Status status, void * data, U8 length)
{
	Response response;
	response.status = status;
	response.length = length;

	response.checksum = response.status ^ response.length;
	char * bytes = (char *)data;

	for (U8 i = 0; i < length; i++)
	{
		response.checksum ^= bytes[i];
	}

	uart_transmit(&response, sizeof(response));
	uart_transmit(data, length);
}
