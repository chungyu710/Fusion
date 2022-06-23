#include "tests/endian.h"

#include <xc.h>
#include <pic16f690.h>
#include <stdio.h>

#include "types.h"
#include "system.h"

void test_endian(void)
{
	system_initialize();

	U8 bytes [] = {0xAB, 0xCD};
	U16 value = *(U16 *)bytes;

	printf("\r\n");
	printf("U8 []: [0x%X, 0x%X]\r\n", bytes[0], bytes[1]);
	printf("U16: 0x%X\r\n", value);

	if (value == 0xCDAB)
	{
		printf("LITTLE ENDIAN\r\n");
	}
	else if (value == 0xABCD)
	{
		printf("BIG ENDIAN\r\n");
	}
	else
	{
		printf("Could not determine endianness\r\n");
	}

	while (1);
}
