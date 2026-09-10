#ifndef ROS2_TRAINING_CPP__GREETING_HPP_
#define ROS2_TRAINING_CPP__GREETING_HPP_

#include <cstddef>
#include <string>

namespace ros2_training_cpp
{
inline std::string make_message(const std::size_t count)
{
  return "Hello World: " + std::to_string(count);
}
}  // namespace ros2_training_cpp

#endif  // ROS2_TRAINING_CPP__GREETING_HPP_
