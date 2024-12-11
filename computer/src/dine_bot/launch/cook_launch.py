from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dine_bot',
            executable='db_manager.py',
            name='db_manager',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='esp32_control_node.py',
            name='esp32_control_node',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='monitor_plc_node.py',
            name='monitor_plc_node',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='mycobot_controller.py',
            name='mycobot_controller',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='suction_cup_node.py',
            name='suction_cup_node',
            output='screen'
        ),
        Node(
            package='dine_bot',
            executable='task_manager.py',
            name='task_manager',
            output='screen'
        )
    ])
