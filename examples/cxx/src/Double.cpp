// Double.cpp

#include <iostream>
#include "Double.h"

// -----
// Double
// -----

Double::Double() :
    _value(0) {};

// ---
// double once
// ---

void Double::one_x(uint32_t x) {
    _value = x * x;
}

// -----
// clear
// -----

void Double::clear() {
    _value = 0;
}

// -----------
// get_value
// -----------

int Double::get_value() {
    return _value;
}