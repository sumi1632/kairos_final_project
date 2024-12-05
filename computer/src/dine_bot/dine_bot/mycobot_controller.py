import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from custom_msgs.action import Cook
import time

class CookActionServer(Node):

    def __init__(self):
        super().__init__('mycobot_controller')
        self._action_server = ActionServer(
            self,
            Cook,
            'start_cook',
            execute_callback=self.execute_callback
        )
        self.get_logger().info('mycobot_controller is ready.')

    async def execute_callback(self, goal_handle):
        menu_name = goal_handle.request.menu_name
        self.get_logger().info(f'Received cooking request for: {menu_name}')

        feedback_msg = Cook.Feedback()
        feedback_statuses = ['Preparing', 'Cooking', 'Plating']

        # Simulate cooking process with feedback updates
        for status in feedback_statuses:
            feedback_msg.cook_status = status
            self.get_logger().info(f'Feedback: {status}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(2)

        # Cooking complete
        result = Cook.Result()
        result.cook_result = f'Cooking for {menu_name} is completed!'
        self.get_logger().info(result.cook_result)

        goal_handle.succeed()

        return result


def main(args=None):
    rclpy.init(args=args)
    cook_action_server = CookActionServer()
    try:
        rclpy.spin(cook_action_server)
    except KeyboardInterrupt:
        cook_action_server.get_logger().info('Cook Action Server shutting down.')
    finally:
        cook_action_server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

