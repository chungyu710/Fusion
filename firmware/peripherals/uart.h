#ifndef UART_H
#define UART_H

void uart_initialize(void);
void uart_transmit(void * data, unsigned int size);
void uart_receive(void * data, unsigned int size);

#endif /* UART_H */
