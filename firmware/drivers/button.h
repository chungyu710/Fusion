#ifndef BUTTON_H
#define BUTTON_H

#include <stdbool.h>

void button_initialize(void);
bool button_pressed(void);
bool button_released(void);

#endif /* BUTTON_H */
