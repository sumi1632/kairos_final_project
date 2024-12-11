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

        # /cmd_vel 토픽 퍼블리셔 생성
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

        # 노란색 물체의 최소 면적 설정
        self.min_contour_area = 350  # 물체 최소 크기 (픽셀 단위)

        self.get_logger().info("Line Tracer Node with ROI started.")

    def image_callback(self, msg):
        # ROS Image 메시지를 OpenCV 이미지로 변환
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # 이미지를 처리하여 노란색 라인 추적
        self.process_image(frame)

    def process_image(self, frame):
        # 이미지 크기 저장
        self.image_height, self.image_width = frame.shape[:2]

        # 화면의 절반부터 아래쪽까지만 ROI로 설정
        roi = frame[self.image_height // 2:, :]

        # 이미지를 HSV 색상 공간으로 변환
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # 노란색 범위 정의
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])

        # 노란색 마스크 생성
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # 작은 노이즈 제거 (모폴로지 연산)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # 마스크에서 컨투어(윤곽선) 추출
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # 특정 크기 이상의 컨투어만 필터링
            valid_contours = [c for c in contours if cv2.contourArea(c) >= self.min_contour_area]

            if valid_contours:
                # 가장 큰 컨투어를 선택
                largest_contour = max(valid_contours, key=cv2.contourArea)

                # 컨투어의 중심 계산
                M = cv2.moments(largest_contour)
                if M['m00'] > 0:
                    self.line_center_x = int(M['m10'] / M['m00'])

                    # 이동 명령 발행
                    self.publish_cmd_vel()
                    return

        # 노란색 물체가 없거나 면적이 작을 경우 정지
        self.stop_robot()
        cv2.imshow("mask",mask)
        cv2.waitKey(10)

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
        if abs(offset) < 20:  # 오프셋이 작으면 직진
            msg.linear.y = 0.0
            msg.angular.z = 0.0
        elif offset > 20:  # 라인이 오른쪽에 있으면 오른쪽으로 이동
            msg.linear.y = -0.1
            msg.angular.z = -0.1  # 오른쪽으로 약간 회전
        elif offset < -20:  # 라인이 왼쪽에 있으면 왼쪽으로 이동
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

def main(args=None):
    rclpy.init(args=args)
    node = LineTracer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Line Tracer Node...")
    finally:
        cv2.destroyAllWindows()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

