#include "uart.h"

#include <xc.h>

#include "fifo.h"

#define RX_BUFFER_SIZE   8
static char rx_buffer [RX_BUFFER_SIZE];
 FIFO rx_fifo;

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

  INTCONbits.GIE = 1;
  INTCONbits.PEIE = 1;
  PIE1bits.RCIE = 1;

  fifo_initialize(&rx_fifo, &rx_buffer, sizeof(rx_buffer));
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
    //if (RCSTAbits.OERR == 1)   // Reset receiver if RX buffer is overrun
    //{
    //  RCSTAbits.CREN = 0;
    //  RCSTAbits.CREN = 1;
    //  led_blink_forever(); < prefer this cause overrun should not happen, host must reset
    //}

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
#include "led.h"
void __interrupt() isr(void)
{
  if (PIR1bits.RCIF)
  {
    if (RCSTAbits.OERR == 1)   // Reset receiver if RX buffer is overrun
    {
      RCSTAbits.CREN = 0;
      RCSTAbits.CREN = 1;
      led_blink_forever();
    }

    //led_on();
    //_delay(10000);
    //led_off();

    if (fifo_is_full(&rx_fifo))
    {
      led_blink_forever();
    }
    else
    {
      fifo_write(&rx_fifo, RCREG);
    }

    //char buf;
    //uart_receive(&buf, 1);
    //uart_transmit(&buf, 1);
  }
}

#include <stdio.h>
void uart_vomit(void)
{
  if (!fifo_is_empty(&rx_fifo))
  {
    printf("[%u], %c\r\n", rx_fifo.length, fifo_read(&rx_fifo));
  }
}
