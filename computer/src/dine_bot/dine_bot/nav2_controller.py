import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from geometry_msgs.msg import PoseStamped, Twist
from custom_msgs.action import Serve
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
                (-0.1533, 0.0476, 1.7359),
                (-0.3437, 0.6820, 1.5708),
                (-0.3014, 0.8512, 1.6421)
            ],
            "2": [(3.0, 0.0, 0.0), (4.0, -1.0, 1.57)]
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
                    (-0.2970, 0.6570, 3.1416),
                    (-1.0050, 0.7110, -1.5308),
                    (-0.9810, 0.1170, -0.0000)
                   
                ]
            elif self.last_location == "2":
                self.paths["0"] = [(1.0, -1.0, 0.0), (2.0, -2.0, 3.14)]
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

        # 네비게이션이 끝난 후 라인트레이싱 활성화 (예: 10초 동안 활성화)
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

        if result.status == 3 or result.status == 4 or result.status == 6:
            self.get_logger().info('Navigation goal succeeded.')
            return True
        else:
            self.get_logger().error(f'Navigation goal failed. {result.status}')
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
        	if active_pixels < 100:  # 활성 픽셀 수가 충분히 작으면 정지
        	    self.get_logger().info('Yellow line not detected or insufficient. Stopping AGV.')
        	    self.cmd_vel_publisher.publish(Twist())  # 정지
        	    return

        # 무게중심 계산
        	moments = cv2.moments(mask)
        	if moments['m00'] > 0:
        	    cx = int(moments['m10'] / moments['m00'])
        	    cy = int(moments['m01'] / moments['m00'])
	
            # AGV 제어
        	    twist = Twist()
        	    error = cx - (cv_image.shape[1] // 2)

            # 선형 속도 및 회전 속도 조정 (회전 반응을 완화)
        	    twist.linear.x = 0.05  # 기본 선형 속도
        	    twist.angular.z = -error / 100.0  # 회전 속도를 완화 (100 -> 300으로 조정)
        	    self.cmd_vel_publisher.publish(twist)

            # 디버깅 정보 출력
        	    self.get_logger().info(f'Center: ({cx}, {cy}), Error: {error}, Twist: linear.x={twist.linear.x}, angular.z={twist.angular.z}')
        	else:
        	    self.get_logger().info('Yellow line not detected. Stopping AGV.')
        	    self.cmd_vel_publisher.publish(Twist())  # 정지

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

