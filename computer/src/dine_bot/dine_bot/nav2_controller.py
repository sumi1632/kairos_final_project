import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from geometry_msgs.msg import PoseStamped, Twist
from my_custom_msgs.action import Serve
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
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
                (-0.3642, 0.0091, 1.5708),
                (-0.3824, 0.7860, 1.5708),
                (-0.3460, 0.9803, 1.5708)
            ],
            "2": [
               (0.3332, 0.0581, -0.0000),
               (0.7981, 0.0814, -0.0000),
               (1.4256, 0.0968, -0.0000),
               (1.7666, 0.1976, 1.6234),
               (1.7433, 0.9491, 1.5708)
            ]
        }

        # 상태 변수 초기화
        self.current_path = []
        self.last_location = None
        self.line_tracing_active = False

        # 라인트레이싱 관련
        self.bridge = CvBridge()
        self.create_subscription(Image, 'myagv/camera/image_raw', self.image_callback, 10)
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # 라인트레이싱 타이머 초기화
        self.line_tracing_timer = None

        # 추가된 변수들
        self.error_buffer = []
        self.buffer_size = 5  # 이동 평균 필터 창 크기
        self.lost_line_count = 0
        self.MAX_LOST_COUNT = 5

        # 상수 정의
        self.LINE_TRACING_LINEAR_SPEED = 0.05
        self.LINE_TRACING_ANGULAR_GAIN = 1.0 / 100.0
        self.LINE_TRACING_ACTIVE_PIXELS_THRESHOLD = 100
        self.MAX_ANGULAR_SPEED = 0.5

        self.get_logger().info('Navigation2 Controller Node Initialized')

    def start_line_tracing(self, duration_sec):
        """라인 트레이싱 활성화 및 타이머 설정."""
        self.line_tracing_active = True
        self.get_logger().info(f'Line tracing activated for {duration_sec} seconds.')

        # 타이머 설정
        if self.line_tracing_timer:
            self.line_tracing_timer.cancel()  # 기존 타이머 취소

        self.line_tracing_timer = self.create_timer(duration_sec, self.disable_line_tracing)

    def disable_line_tracing(self):
        """라인 트레이싱 비활성화."""
        self.line_tracing_active = False
        self.get_logger().info('Line tracing deactivated.')
        self.cmd_vel_publisher.publish(Twist())
        if self.line_tracing_timer:
            self.line_tracing_timer.cancel()  # 타이머 정리
            self.line_tracing_timer = None

    async def execute_serve_callback(self, goal_handle):
        """start_serve 액션 서버의 콜백 함수."""
        self.line_tracing_active = False  # 네비게이션 중 라인트레이싱 비활성화
        table_num = str(goal_handle.request.table_num)
        self.get_logger().info(f'Received serve request for table: {table_num}')

        # 초기 위치로 돌아올 때
        if table_num == "0":
            if self.last_location == "1":
                self.paths["0"] = [
                    (-0.2489, 0.7618, -3.1059),
                    (-1.0440, 0.6950, -1.5708),
                    (-1.0076, -0.1548, -0.0000)
                ]
            elif self.last_location == "2":
                self.paths["0"] = [
                    (1.7356, 1.9409, -3.0792),
                    (0.8678, 1.9564, -3.1083),
                    (0.2712, 1.9719, 3.1416),
                    (-0.8910, 1.9796, -1.5708),
                    (-0.9065, 1.0499, -1.5708),
                    (-0.9375, 0.5152, -1.5182),
                    (-0.9530, -0.1898, -0.0000)
                ]
            else:
                self.get_logger().error('경로를 설정할 수 없습니다. 현재 위치가 초기 위치인지 확인하세요.')
                goal_handle.abort()
                return Serve.Result(move_result='failed')

        # 경로 확인
        if table_num not in self.paths:
            self.get_logger().error(f'Unknown table number: {table_num}')
            goal_handle.abort()
            return Serve.Result(move_result='failed')

        self.current_path = self.paths[table_num]

        for index, (x, y, yaw) in enumerate(self.current_path):
            pose = self.create_pose(x, y, yaw)
            success = await self.send_goal(pose)

            if not success:
                self.get_logger().error(f'Failed to reach waypoint {index + 1}')
                goal_handle.abort()
                return Serve.Result(move_result='failed')

            # 피드백 전송
            feedback = Serve.Feedback()
            feedback.x = x
            feedback.y = y
            feedback.theta = yaw
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'Waypoint {index + 1}/{len(self.current_path)} reached.')

        self.last_location = table_num
        self.get_logger().info(f'Successfully served table: {table_num}')
        goal_handle.succeed()

        # 네비게이션이 끝난 후 라인트레이싱 활성화 (예: 15초 동안 활성화)
        self.start_line_tracing(duration_sec=15)
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

        if result.status in [GoalStatus.STATUS_SUCCEEDED]:
            self.get_logger().info('Navigation goal succeeded.')
            return True
        else:
            self.get_logger().error(f'Navigation goal failed with status: {result.status}')
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

    def image_callback(self, msg):
        if not self.line_tracing_active:
            return

        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

            # 노란색 범위 정의 (조정 가능)
            lower_yellow = (20, 100, 100)
            upper_yellow = (40, 255, 255)
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

            # 노란색 라인을 인식하지 못할 경우 정지
            active_pixels = cv2.countNonZero(mask)
            if active_pixels < self.LINE_TRACING_ACTIVE_PIXELS_THRESHOLD:
                self.get_logger().info('Yellow line not detected or insufficient. Stopping AGV.')
                self.cmd_vel_publisher.publish(Twist())  # 정지
                return

            # 무게중심 계산
            moments = cv2.moments(mask)
            if moments['m00'] > 0:
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])

                # 오류 계산
                error = cx - (cv_image.shape[1] // 2)

                # 오류 버퍼 업데이트
                self.error_buffer.append(error)
                if len(self.error_buffer) > self.buffer_size:
                    self.error_buffer.pop(0)

                # 이동 평균 필터 적용
                avg_error = sum(self.error_buffer) / len(self.error_buffer)

                # AGV 제어 (이동 평균 필터 적용된 오류 사용)
                twist = Twist()
                twist.linear.x = self.LINE_TRACING_LINEAR_SPEED
                twist.angular.z = -avg_error * self.LINE_TRACING_ANGULAR_GAIN

                # 회전 속도 제한
                twist.angular.z = max(min(twist.angular.z, self.MAX_ANGULAR_SPEED), -self.MAX_ANGULAR_SPEED)

                self.cmd_vel_publisher.publish(twist)

                # 디버깅 정보 출력
                self.get_logger().info(
                    f'Center: ({cx}, {cy}), Error: {error}, '
                    f'Avg Error: {avg_error:.2f}, Twist: linear.x={twist.linear.x}, angular.z={twist.angular.z:.4f}'
                )
            else:
                self.lost_line_count += 1
                if self.lost_line_count >= self.MAX_LOST_COUNT:
                    self.get_logger().info('Yellow line not detected consistently. Stopping AGV.')
                    self.cmd_vel_publisher.publish(Twist())  # 정지
                    self.lost_line_count = 0
        except Exception as e:
            self.get_logger().error(f'Image processing error: {e}', exc_info=True)


def main():
    rclpy.init()

    node = Navigation2Controller()

    # ROS 2 스핀: 액션 서버 처리
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()

