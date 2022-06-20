#ifndef UART_H
#define UART_H

#include "types.h"

void uart_initialize(void);
void uart_transmit(void * data, U8 length);
void uart_receive(void * data, U8 length);

#endif /* UART_H */
