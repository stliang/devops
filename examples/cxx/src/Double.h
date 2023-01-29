// Double.h

#ifndef CMAKE_GCOV_CALCULATOR_H_
#define CMAKE_GCOV_CALCULATOR_H_

#include <iostream>

class Double {
private:
    uint32_t _value;

public:
    // -----
    // Double
    // -----

    Double();

    // ---
    // double once
    // ---

    void one_x(uint32_t x);

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
