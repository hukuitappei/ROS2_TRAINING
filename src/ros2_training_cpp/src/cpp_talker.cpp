#include <chrono>
#include <cstddef>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "ros2_training_cpp/greeting.hpp"
#include "std_msgs/msg/string.hpp"

class TrainingTalker : public rclcpp::Node
{
public:
  TrainingTalker() : Node("cpp_talker"), count_(0)
  {
    const auto topic_name = declare_parameter<std::string>("topic_name", "training/chatter");
    const auto period_ms = declare_parameter<int>("publish_period_ms", 500);
    publisher_ = create_publisher<std_msgs::msg::String>(topic_name, 10);
    timer_ = create_wall_timer(
      std::chrono::milliseconds(period_ms),
      std::bind(&TrainingTalker::publish_message, this));
  }

private:
  void publish_message()
  {
    std_msgs::msg::String message;
    message.data = ros2_training_cpp::make_message(count_++);
    RCLCPP_INFO(get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher_->publish(message);
  }
  std::size_t count_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<TrainingTalker>());
  rclcpp::shutdown();
  return 0;
}
