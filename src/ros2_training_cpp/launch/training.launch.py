from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    cpp_share = FindPackageShare("ros2_training_cpp")
    py_share = FindPackageShare("ros2_training_py")
    return LaunchDescription([
        Node(package="ros2_training_cpp", executable="cpp_talker", name="cpp_talker",
             parameters=[PathJoinSubstitution([cpp_share, "config", "talker.yaml"])],
             output="screen"),
        Node(package="ros2_training_py", executable="py_listener", name="py_listener",
             parameters=[PathJoinSubstitution([py_share, "config", "listener.yaml"])],
             output="screen"),
    ])
