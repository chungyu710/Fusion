#ifndef SPI_H
#define SPI_H

#include "types.h"

void spi_initialize(void);
void spi_select(void);
void spi_release(void);
void spi_transmit(void * data, U8 length);
void spi_receive(void * data, U8 length);

#endif /* SPI_H */
