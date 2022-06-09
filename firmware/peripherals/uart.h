#ifndef UART_H
#define UART_H

void uart_initialize(void);
void uart_transmit(void * buffer, unsigned int size);
void uart_receive(void * buffer, unsigned int size);

#endif /* UART_H */
