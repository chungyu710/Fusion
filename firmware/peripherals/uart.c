#include "uart.h"

#include <xc.h>

void uart_initialize(void) {
  // initilaize the SPBRGH, SPBRG register pair and the BRGH and BRG16 bits to achieve the desired baud rate of 9600 bits/sec
	TXSTAbits.BRGH    = 1;
	BAUDCTLbits.BRG16 = 1;
	SPBRGH            = 0;
	SPBRG             = 16;  // this is the calculated value based on 115200 baud and 8 MHz clk

	TXSTAbits.TXEN    = 1;		// enables transmitter circuitry
	RCSTAbits.CREN    = 1;		// enables receiver circuitry
	TXSTAbits.SYNC    = 0;		// configures to async operation
	RCSTAbits.SPEN    = 1;		// enables EUSART and sets TX/CK pin as an output
}

void uart_transmit(void * data, U8 length) {
  char * ch = (char*)data;      // cast data element to char pointer

  for(int i = 0; i < length; i++) {
    while(!PIR1bits.TXIF) {}    // wait for the TXIF to be cleared, indicating the TXREG is empty, before writing
    TXREG = ch[i];	            // load 8-bit data into the TXREG regsiter to start the transmission
  }
}

void uart_receive(void * data, U8 length) {
  char * ch = (char*)data;       // cast data element to char pointer

  for(int i = 0; i < length; ) {
    if(PIR1bits.RCIF) {
      // if the RCIF is set, there is an unread character in the receive FIFO
      ch[i] = RCREG;
      i++;
    }
  }
}

void putch(char data) {
  uart_transmit(&data, 1);
}
