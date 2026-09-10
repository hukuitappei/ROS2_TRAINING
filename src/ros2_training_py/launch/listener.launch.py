from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    package_share = FindPackageShare("ros2_training_py")
    return LaunchDescription([
        Node(
            package="ros2_training_py",
            executable="py_listener",
            name="py_listener",
            parameters=[PathJoinSubstitution([package_share, "config", "listener.yaml"])],
            output="screen",
        )
    ])
