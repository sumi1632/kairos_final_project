import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from geometry_msgs.msg import PoseStamped
from custom_msgs.action import Serve  # Serve 액션 타입
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
import math


class Navigation2Controller(Node):
    def __init__(self):
        super().__init__('nav2_controller')

        # NavigateToPose 액션 클라이언트
        self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # start_serve 액션 서버 생성
        self.serve_action_server = ActionServer(
            self,
            Serve,
            'start_serve',
            execute_callback=self.execute_serve_callback
        )

        # 이동 경로 정의
        self.paths = {
            "1": [
                (1.6990, 0.7886, 2.9598),
                (1.2841, 0.7027, 2.8950),
                (1.1347, 0.7642, 2.9330),
                (0.8418, 0.8691, 2.9010)
            ],
            "2": [
            	(2.0551, 1.2366, 1.4135),
                (1.9939, 1.6593, 1.4536),
                (2.0198, 2.1695, 1.5607),
                (1.9779, 2.4620, 2.5248),
                (1.6504, 2.6046, 2.9127),
                (1.7239, 2.5339, -0.3670)
            ]
        }

        # 현재 상태 변수 초기화
        self.current_path = []  # 현재 경로
        self.last_location = None  # 마지막 위치

        self.get_logger().info('Navigation2 Controller Node Initialized')

    async def execute_serve_callback(self, goal_handle):
        """start_serve 액션 서버의 콜백 함수."""
        table_num = str(goal_handle.request.table_num)
        self.get_logger().info(f'Received serve request for table: {table_num}')

        # 경로 동적 설정 (location_callback의 동작 포함)
        if table_num == "0":
            if self.last_location == "1":
                self.paths["0"] = [
                    (0.9758, 0.4718, -1.9208),
                    (0.6946, -0.0414, -1.8652),
                    (0.6100, -0.1006, -0.3500),
                    (1.3568, -0.4261, -0.3475),
                    (1.4470, -0.4090, 1.2397),
                    (1.6865, 0.1346, 1.1998),
                    (1.8006, 0.6148, 1.2130)
                ]
            elif self.last_location == "2":
                self.paths["0"] = [
                    (1.9392, 2.4355, 2.6607),
                    (1.3115, 2.6631, 2.7886),
                    (0.9592, 2.8064, 3.0926),
                    (0.6008, 2.7519, -2.2161),
                    (0.3717, 2.1348, -1.8489),
                    (0.2415, 1.4545, -1.6451),
                    (0.0584, 0.8516, -1.8217),
                    (-0.1390, 0.3524, -1.8217),
                    (-0.1403, 0.2156, -0.2764),
                    (0.5965, 0.0629, -0.3670),
                    (1.0980, -0.0818, -0.3670),
                    (1.3566, -0.1814, -0.2292),
                    (1.4344, -0.0414, 1.2566),
                    (1.9050, 0.6159, 1.1923),
                    (1.8006, 0.6148, 1.2130)
                ]
            else:
                self.get_logger().error('경로를 설정할 수 없습니다. 현재 위치가 초기 위치인지 확인하세요.')
                goal_handle.abort()
                return Serve.Result(move_result=f'last_location: {self.last_location} 0 location failed')

        # 경로 확인
        if table_num not in self.paths:
            self.get_logger().error(f'Unknown table number: {table_num}')
            goal_handle.abort()
            return Serve.Result(move_result='table_num not in self.paths failed')

        # 이동 경로 설정
        self.current_path = self.paths[table_num]

        for index, (x, y, yaw) in enumerate(self.current_path):
            pose = self.create_pose(x, y, yaw)
            success = await self.send_goal(pose)

            if not success:
                self.get_logger().error(f'Failed to reach waypoint {index + 1}')
                goal_handle.abort()
                return Serve.Result(move_result='reach waypoint failed')

            # 피드백 전송
            feedback = Serve.Feedback()
            feedback.x = x
            feedback.y = y
            feedback.theta = yaw
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'Waypoint {index + 1}/{len(self.current_path)} reached.')

        self.last_location = table_num  # 마지막 위치 업데이트
        self.get_logger().info(f'Successfully served table: {table_num}')
        goal_handle.succeed()
        return Serve.Result(move_result='success')

    async def send_goal(self, pose: PoseStamped):
        """NavigateToPose 액션 클라이언트를 통해 목표로 이동."""
        if not self.nav_action_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('NavigateToPose action server not available.')
            return False

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose

        self.get_logger().info(f'Sending navigation goal: x={pose.pose.position.x}, y={pose.pose.position.y}')
        send_goal_future = self.nav_action_client.send_goal_async(goal_msg)
        goal_handle = await send_goal_future

        if not goal_handle.accepted:
            self.get_logger().error('Navigation goal rejected.')
            return False

        self.get_logger().info('Navigation goal accepted.')
        result_future = goal_handle.get_result_async()
        result = await result_future
        print(f"Goal handle status before result: {goal_handle.status}")
        if result.status == 3 or result.status == 6:
            self.get_logger().info('Navigation goal succeeded.')
            return True
        else:
            self.get_logger().error('Navigation goal failed.')
            self.get_logger().error(f'{result.status}')
            return False

    def create_pose(self, x, y, yaw):
        """Create a PoseStamped message for a given x, y, yaw."""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = x
        pose.pose.position.y = y

        # Orientation을 yaw 값으로 설정
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)

        return pose

def main():
    rclpy.init()

    node = Navigation2Controller()

    # ROS 2 스핀: 액션 서버 처리
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()

