#ifndef SPI_H
#define SPI_H

void spi_initialize(void);
void spi_transmit(void * buffer, unsigned int size);
void spi_receive(void * buffer, unsigned int size)

#endif /* SPI_H */
