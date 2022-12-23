#include "gtest/gtest.h"
#include "../src/Adder.h"

TEST(Foo, Adder_add)
{
  Adder adder;
  adder.add(5);
  EXPECT_EQ(5, adder.get_value());
}

TEST(Foo, Adder_clear)
{
  Adder adder;
  adder.add(5);
  adder.clear();
  EXPECT_EQ(0, adder.get_value());
}