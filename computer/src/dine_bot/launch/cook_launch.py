from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dine_bot',
            executable='db_manager_node',
            name='db_manager_node',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='esp32_control_node',
            name='esp32_control_node',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='monitor_plc_node',
            name='monitor_plc_node',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='mycobot_controller',
            name='mycobot_controller',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='suction_cup_node',
            name='suction_cup_node',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='task_manager_node',
            name='task_manager_node',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='plate_distance_node',
            name='plate_distance_node',
            output='screen'
        )
    ])
