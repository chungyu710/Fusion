#ifndef UART_H
#define UART_H

#include "types.h"

void uart_initialize(void);
void uart_transmit(void const * data, U16 length);
void uart_receive(void * data, U16 length);

#endif /* UART_H */
