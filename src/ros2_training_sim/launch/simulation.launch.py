import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context):
    package_share = get_package_share_directory("ros2_training_sim")
    ros_gz_share = get_package_share_directory("ros_gz_sim")
    world = os.path.join(package_share, "worlds", "training_world.sdf")
    bridge_config = os.path.join(package_share, "config", "bridge.yaml")
    headless = LaunchConfiguration("headless").perform(context).lower() == "true"
    gz_args = f"-r {'-s ' if headless else ''}{world}"

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_share, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": gz_args}.items(),
    )
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="ros_gz_bridge",
        parameters=[{"config_file": bridge_config}],
        output="screen",
    )
    lidar_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="lidar_static_transform",
        arguments=[
            "--x", "0.10",
            "--z", "0.11",
            "--frame-id", "base_link",
            "--child-frame-id", "training_robot/lidar_link/lidar",
        ],
        output="screen",
    )
    return [gazebo, bridge, lidar_tf]


def generate_launch_description():
    package_share = get_package_share_directory("ros2_training_sim")
    model_path = os.path.join(package_share, "models")
    existing_path = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    os.environ["GZ_SIM_RESOURCE_PATH"] = os.pathsep.join(
        path for path in [model_path, existing_path] if path
    )
    return LaunchDescription([
        DeclareLaunchArgument(
            "headless",
            default_value="false",
            description="Run the Gazebo server without its GUI.",
        ),
        OpaqueFunction(function=launch_setup),
    ])
