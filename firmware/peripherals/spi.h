#ifndef SPI_H
#define SPI_H

void spi_initialize(void);
void spi_transmit(void * data, unsigned int size);
void spi_receive(void * data, unsigned int size)

#endif /* SPI_H */
