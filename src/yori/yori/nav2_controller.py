import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import String  # 메시지 타입 추가


class Navigation2Controller(Node):
    def __init__(self):
        super().__init__('nav2_controller')
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # 목표 위치를 수신하는 토픽 구독
        self.subscription = self.create_subscription(
            String,  # 토픽 메시지 타입
            'move_to_location',  # 토픽명
            self.location_callback,  # 콜백 함수
            10  # 큐 사이즈
        )

        # 경유지를 포함한 이동 경로 정의
        self.paths = {
            "A": [
		    (2.4641, -1.4520, -1.57),  # 첫 번째 경유지
		    (2.4708, -1.9828, -1.58),  # 두 번째 경유지
		    (2.4708, -2.4331, -1.57)   # 세 번째 경유지
		],
            "B": [(3.0, 0.0, 0.0), (4.0, -1.0, 1.57)]  # B까지의 경유지
        }

        # C 경로는 동적으로 결정됨
        self.current_path = []  # 현재 이동 경로 저장
        self.current_target_index = 0  # 현재 목표 인덱스
        self.last_location = None  # 마지막 위치 저장

    def send_goal(self, pose: PoseStamped):
        """Send a goal to Navigation2."""
        if not self.action_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('Action server not available. Is Navigation2 running?')
            return False

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose

        self.get_logger().info(f'Sending goal: {pose.pose.position}')
        future = self.action_client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)
        return True

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected by the server.')
            return

        self.get_logger().info('Goal accepted. Waiting for result...')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        if result:
            self.get_logger().info('Goal reached successfully!')
            self.move_to_next_target()
        else:
            self.get_logger().error('Failed to reach the goal.')

    def location_callback(self, msg):
        """Callback function for receiving location names."""
        location_name = msg.data.strip().upper()  # 받은 메시지 데이터 처리
        self.get_logger().info(f'Received location: {location_name}')

        # C 경로 동적 생성
        if location_name == "C":
            if self.last_location == "A":
                self.paths["C"] = [
		    (2.4756, -2.6657, 0.03),   # 첫 번째 경유지
		    (3.2210, -2.6366, 0.03),   # 두 번째 경유지
		    (3.2273, -2.6230, 1.57),   # 세 번째 경유지
		    (3.2277, -1.9641, 1.59),   # 네 번째 경유지
		    (3.2040, -1.4001, 1.59),   # 다섯 번째 경유지
		    (3.2036, -1.3867, 3.10),   # 여섯 번째 경유지
		    (2.6388, -1.3579, 3.09)    # 일곱 번째 경유지
		]
            elif self.last_location == "B":
                self.paths["C"] = [(1.0, -1.0, 0.0), (2.0, -2.0, 3.14)]  # B에서 돌아오는 C 경로
            else:
                self.get_logger().error('C 경로를 설정할 수 없습니다. 마지막 위치를 확인하세요.')
                return

        # 위치가 사전에 정의된 경우
        if location_name in self.paths:
            self.current_path = self.paths[location_name]  # 이동 경로 설정
            self.current_target_index = 0  # 경유지 초기화
            self.get_logger().info(f'Navigating to {location_name} with waypoints: {self.current_path}')
            self.move_to_next_target()
            self.last_location = location_name  # 마지막 위치 업데이트
        else:
            self.get_logger().error(f'Unknown location: {location_name}. Available: {list(self.paths.keys())}')

    def move_to_next_target(self):
        """Move to the next target in the current path."""
        if self.current_target_index < len(self.current_path):
            x, y, yaw = self.current_path[self.current_target_index]
            pose = self.create_pose(x, y, yaw)
            self.get_logger().info(f'Moving to waypoint {self.current_target_index + 1}/{len(self.current_path)}: x={x}, y={y}, yaw={yaw}')
            self.current_target_index += 1
            self.send_goal(pose)
        else:
            self.get_logger().info('All waypoints reached!')

    def create_pose(self, x, y, yaw):
        """Create a PoseStamped message for a given x, y, yaw."""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        # Orientation을 yaw 값으로 설정 (간단한 예제라 정밀한 변환 생략)
        pose.pose.orientation.z = yaw  # 단순화를 위해 z값으로 yaw 표현
        pose.pose.orientation.w = 1.0  # 기본값
        return pose


def main():
    rclpy.init()

    node = Navigation2Controller()

    # ROS 2 스핀: 토픽 처리
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()

