// Adder.cpp

#include <iostream>
#include "Adder.h"

// -----
// Adder
// -----

Adder::Adder() :
    _value(0) {};

// ---
// add
// ---

void Adder::add(uint32_t x) {
    _value += x;
}

// -----
// clear
// -----

void Adder::clear() {
    _value = 0;
}

// -----------
// get_value
// -----------

int Adder::get_value() {
    return _value;
}