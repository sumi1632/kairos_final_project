import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class LineTracer(Node):
    def __init__(self):
        super().__init__('line_tracer')

        # /cmd_vel 토픽 Publisher 생성
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # 카메라 토픽 구독
        self.camera_subscription = self.create_subscription(
            Image,
            'myagv/camera/image_raw',
            self.image_callback,
            10
        )

        # OpenCV-ROS 브릿지 생성
        self.bridge = CvBridge()

        # 라인 중심 좌표와 이미지 중심 저장 변수
        self.line_center_x = None
        self.image_width = None
        self.image_height = None

        self.get_logger().info('Line Tracer Node with stop functionality started.')

    def image_callback(self, msg):
        # ROS Image 메시지를 OpenCV 이미지로 변환
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # 이미지를 처리하여 노란색 라인 추적
        self.process_image(frame)

    def process_image(self, frame):
        # 이미지 크기 저장
        self.image_height, self.image_width = frame.shape[:2]

        # 이미지를 HSV 색상 공간으로 변환
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 노란색 범위 정의
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # 노란색 마스크 생성
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # 마스크에서 컨투어(윤곽선) 추출
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # 가장 큰 컨투어를 선택
            largest_contour = max(contours, key=cv2.contourArea)

            # 컨투어의 중심 계산
            M = cv2.moments(largest_contour)
            if M['m00'] > 0:
                self.line_center_x = int(M['m10'] / M['m00'])

                # 라인의 중심을 시각적으로 표시 (디버깅용)
                cv2.circle(frame, (self.line_center_x, self.image_height // 2), 5, (0, 255, 0), -1)

                # 이동 명령 발행
                self.publish_cmd_vel()
        else:
            # 라인이 감지되지 않을 경우 정지 명령 발행
            self.stop_robot()

        # 디버깅용: 이미지를 시각적으로 출력
        cv2.imshow("Original Frame", frame)
        cv2.imshow("Yellow Mask", mask)
        cv2.waitKey(1)

    def publish_cmd_vel(self):
        if self.line_center_x is None or self.image_width is None:
            return

        # 이미지 중심 좌표 계산
        image_center_x = self.image_width // 2
        offset = self.line_center_x - image_center_x

        # Twist 메시지 생성
        msg = Twist()

        # 선형 속도 (x축으로 전진)
        msg.linear.x = 0.2  # 전진 속도 설정

        # 각속도 (z축 회전) 또는 측면 이동 (y축 속도)
        if abs(offset) < 10:  # 오프셋이 작으면 직진
            msg.linear.y = 0.0
            msg.angular.z = 0.0
        elif offset > 10:  # 라인이 오른쪽에 있으면 오른쪽으로 이동
            msg.linear.y = -0.1
            msg.angular.z = -0.1  # 오른쪽으로 약간 회전
        elif offset < -10:  # 라인이 왼쪽에 있으면 왼쪽으로 이동
            msg.linear.y = 0.1
            msg.angular.z = 0.1  # 왼쪽으로 약간 회전

        # 메시지 발행
        self.cmd_vel_publisher.publish(msg)
        self.get_logger().info(f"Published cmd_vel: linear.x={msg.linear.x}, linear.y={msg.linear.y}, angular.z={msg.angular.z}")

    def stop_robot(self):
        # 정지 명령 생성
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.angular.z = 0.0

        # 정지 메시지 발행
        self.cmd_vel_publisher.publish(msg)
        self.get_logger().warn("No line detected. Robot stopped.")


def main(args=None):
    rclpy.init(args=args)
    node = LineTracer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Line Tracer Node...')
    finally:
        cv2.destroyAllWindows()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

