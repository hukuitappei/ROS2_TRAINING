"""Launch the sample robot manzai performance."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

from pathlib import Path


def generate_launch_description() -> LaunchDescription:
    default_script = str(
        Path(get_package_share_directory('robot_manzai'))
        / 'config'
        / 'sample_manzai.yaml'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'script_file',
            default_value=default_script,
            description='Path to a manzai script YAML file.',
        ),
        DeclareLaunchArgument(
            'repeat',
            default_value='false',
            description='Repeat the script after the final line.',
        ),
        Node(
            package='robot_manzai',
            executable='manzai_node',
            name='manzai_node',
            output='screen',
            parameters=[{
                'script_file': LaunchConfiguration('script_file'),
                'repeat': LaunchConfiguration('repeat'),
            }],
        ),
    ])
