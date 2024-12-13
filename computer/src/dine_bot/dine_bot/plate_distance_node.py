import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from ultralytics import YOLO
import os
from ament_index_python.packages import get_package_share_directory

class PlateDistanceService(Node):
    def __init__(self):
        super().__init__('plate_distance_node')

        # YOLO 모델 로드
        model_path = os.path.join(get_package_share_directory('dine_bot'), 'models', 'best.pt')
        self.model = YOLO(model_path)

        # 카메라 설정
        self.cap = cv2.VideoCapture(2)

        # 실제 객체 크기 및 카메라 매트릭스 설정
        self.actual_object_width_mm = 165  # 접시의 실제 너비 (단위: mm)
        self.camera_matrix = np.array([[561.20581683, 0., 353.85748295],
                                       [0., 564.8824937, 221.57289288],
                                       [0., 0., 1.]])
        self.dist_coeffs = np.array([[0.23935691, -0.71647137, -0.01530787, 0.01102398, 0.39847327]])

        # 서비스 서버 생성
        self.srv = self.create_service(Trigger, 'get_plate_distance', self.handle_service_request)
        self.get_logger().info("Plate Distance Service Ready")

    def calculate_distance_to_object(self, width_in_pixels):
        """객체의 너비 픽셀 값을 통해 거리 계산"""
        focal_length = self.camera_matrix[0, 0]  # Focal length in pixels
        distance = (self.actual_object_width_mm * focal_length) / width_in_pixels
        return distance

    def detect_plate_yolo(self, frame):
        """YOLO를 이용한 접시 탐지"""
        results = self.model.predict(frame, stream=True)
        largest_box = None
        largest_area = 0
        largest_class_name = ""

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                if class_id == 0:  # 클래스 ID 0이 접시로 설정되어 있다고 가정
                    class_name = "plate"
                else:
                    continue
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)
                
                if area > 2000 and area > largest_area:  # 최소 면적 조건 추가
                    largest_area = area
                    largest_box = (x1, y1, x2, y2)
                    largest_class_name = class_name

        if largest_box:
            x1, y1, x2, y2 = largest_box
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            width_in_pixels = x2 - x1
            return (cx, cy, width_in_pixels, largest_class_name, x1, y1, x2, y2)
        return None

    def handle_service_request(self, request, response):
        """서비스 요청 처리 콜백"""
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error("카메라에서 프레임을 읽을 수 없습니다.")
            response.success = False
            response.message = "Failed to capture frame from camera"
            return response

        result = self.detect_plate_yolo(frame)
        if result:
            cx, cy, width_in_pixels, class_name, x1, y1, x2, y2 = result
            distance = self.calculate_distance_to_object(width_in_pixels)
            response.success = True
            response.message = f"{distance:.2f}"
            self.get_logger().info(response.message)
        else:
            response.success = False
            response.message = "No plate detected"
            self.get_logger().info("No plate detected")

        return response

    def destroy(self):
        """리소스 해제"""
        self.cap.release()
        super().destroy()

def main(args=None):
    rclpy.init(args=args)
    node = PlateDistanceService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Plate Distance Service")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
