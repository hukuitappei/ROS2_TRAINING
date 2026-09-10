import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from ros2_training_py.message_format import format_received_message


class TrainingListener(Node):
    def __init__(self) -> None:
        super().__init__("py_listener")
        topic_name = self.declare_parameter(
            "topic_name", "training/chatter"
        ).value
        self.subscription = self.create_subscription(
            String, topic_name, self.listener_callback, 10
        )

    def listener_callback(self, message: String) -> None:
        self.get_logger().info(format_received_message(message.data))


def main(args=None) -> None:
    rclpy.init(args=args)
    node = TrainingListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.destroy_node()
            if rclpy.ok():
                rclpy.shutdown()
        except KeyboardInterrupt:
            # A launch service can forward a second SIGINT during cleanup.
            pass


if __name__ == "__main__":
    main()
