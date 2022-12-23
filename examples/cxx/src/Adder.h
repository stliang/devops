// Adder.h

#ifndef CMAKE_GCOV_CALCULATOR_H_
#define CMAKE_GCOV_CALCULATOR_H_

#include <iostream>

class Adder {
private:
    uint32_t _value;

public:
    // -----
    // Adder
    // -----

    Adder();

    // ---
    // add
    // ---

    void add(uint32_t x);

    // -----
    // clear
    // -----

    void clear();

    //----------
    // get_value
    //----------
    int get_value();

};

#endif
