#include <gtest/gtest.h>
#include "ros2_training_cpp/greeting.hpp"

TEST(Greeting, formats_counter)
{
  EXPECT_EQ(ros2_training_cpp::make_message(0), "Hello World: 0");
  EXPECT_EQ(ros2_training_cpp::make_message(42), "Hello World: 42");
}
