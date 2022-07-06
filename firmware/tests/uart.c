#include "tests/uart.h"

#include <xc.h>
#include <pic16f690.h>

#include "peripherals/uart.h"

void test_uart_echo(void) {
  while(1) {
    char data;
    uart_receive(&data, 1);
    uart_transmit(&data, 1);
  }
}