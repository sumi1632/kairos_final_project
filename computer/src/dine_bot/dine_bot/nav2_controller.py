import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from geometry_msgs.msg import PoseStamped, Twist, PoseWithCovarianceStamped
from custom_msgs.action import Serve
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import math
import time


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
                (-0.3965, 0.0437, 1.5708),
                (-0.3427, 0.7627, 1.5708),
                (-0.3562, 0.9711, 1.5708)
            ],
            "2": [
                (0.6345, 0.0899, -0.0000),
                (1.3324, 0.0582, -0.0000),
                (1.8505, 0.2062, 1.5708),
                (1.8611, 0.9675, 1.5708)
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
        self.buffer_size = 12  # 이동 평균 필터 창 크기
        self.lost_line_count = 0
        self.MAX_LOST_COUNT = 5

        # 상수 정의
        self.LINE_TRACING_LINEAR_SPEED = 0.05
        self.LINE_TRACING_ANGULAR_GAIN = 0.005
        self.LINE_TRACING_ACTIVE_PIXELS_THRESHOLD = 100
        self.MAX_ANGULAR_SPEED = 0.5

        # 초기 위치 게시 관련
        self.initial_pose_publisher = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
        self.publish_initial_pose_once()

        self.get_logger().info('Navigation2 Controller Node Initialized')
        

    def publish_initial_pose_once(self):
        time.sleep(5)
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()

        # Set initial position
        msg.pose.pose.position.x = -0.3489495515823364
        msg.pose.pose.position.y = 0.005288539454340935
        msg.pose.pose.position.z = 0.0

        # Set initial orientation (quaternion)
        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = 0.008193985547100957
        msg.pose.pose.orientation.w = 0.9999664287369121

        # Set covariance
        msg.pose.covariance = [0.1] * 36

        # Publish the message
        self.initial_pose_publisher.publish(msg)
        self.get_logger().info('Published initial pose!')

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
                    (-0.3696, 0.8299, 3.1416),
                    (-1.1491, 0.7829, -1.5708),
                    (-1.0483, 0.1982, -1.5708),
                    (-1.0954, -0.1714, -0.0000)
                ]
            elif self.last_location == "2":
                self.paths["0"] = [
                    (1.9034, 1.5174, 1.5708),
                    (1.9034, 2.0038, 3.1416),
                    (1.2160, 2.0567, 3.1416),
                    (0.6345, 2.0567, 3.1416),
                    (-0.1163, 2.0038, 3.1416),
                    (-0.9517, 2.0567, -1.5941),
                    (-0.9517, 0.9464, -1.5708),
                    (-1.0046, 0.3119, -1.5708),
                    (-1.0046, -0.1216, -0.0000)
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

        # 네비게이션이 끝난 후 라인트레이싱 활성화 (예: 30초 동안 활성화)
        self.start_line_tracing(duration_sec=30)
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

            # 노이즈 제거
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

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
                normalized_error = error / (cv_image.shape[1] // 2)

                twist = Twist()

                if abs(normalized_error) > 0.15:
                    # 중심 맞추기: 측면 이동
                    twist.linear.x = 0.0  # 정지
                    if normalized_error > 0:
                        twist.linear.y = -1 * self.LINE_TRACING_LINEAR_SPEED
                    else:
                        twist.linear.y = self.LINE_TRACING_LINEAR_SPEED
                    twist.angular.z = 0.0
                else:
                    # 위치가 맞으면 앞으로 이동
                    twist.linear.x = self.LINE_TRACING_LINEAR_SPEED
                    twist.linear.y = 0.0  # 측면 이동 비활성화
                    twist.angular.z = 0.0

                self.cmd_vel_publisher.publish(twist)

                # 디버깅 정보 출력
                self.get_logger().info(
                    f'Center: ({cx}, {cy}), Error: {error}, normalized_error: {normalized_error:.2f}'
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

