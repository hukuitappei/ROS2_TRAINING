cmake_minimum_required(VERSION 3.8)
project(ros2_training_cpp)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(cpp_talker src/cpp_talker.cpp)
target_compile_features(cpp_talker PUBLIC cxx_std_17)
target_include_directories(cpp_talker PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
ament_target_dependencies(cpp_talker rclcpp std_msgs)

install(TARGETS cpp_talker DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include)
install(DIRECTORY config launch DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_greeting test/test_greeting.cpp)
  target_include_directories(test_greeting PRIVATE include)
endif()

ament_package()
