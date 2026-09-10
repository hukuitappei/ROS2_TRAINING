cmake_minimum_required(VERSION 3.8)
project(ros2_training_sim)

find_package(ament_cmake REQUIRED)

install(DIRECTORY config launch models worlds
  DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_simulation_files test/test_simulation_files.py)
endif()

ament_package()
