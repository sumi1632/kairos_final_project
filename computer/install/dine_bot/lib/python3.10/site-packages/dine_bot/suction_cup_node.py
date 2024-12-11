import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket

class SuctionControlNode(Node):
    def __init__(self):
        super().__init__('suction_control_node')
        
        # ROS2 Subscriber 및 Publisher 설정
        self.subscription = self.create_subscription(
            String, 'suction_command', self.suction_command_callback, 10)
        self.publisher = self.create_publisher(String, 'suction_response', 10)
        
        # 소켓 서버 설정
        self.server_ip = '0.0.0.0'
        self.server_port = 9000
        self.get_logger().info("Starting server...")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.server_ip, self.server_port))
        self.server.listen(1)
        self.get_logger().info(f"Server listening on {self.server_ip}:{self.server_port}")

        self.client, self.addr = self.server.accept()
        self.get_logger().info(f"Connection from {self.addr}")

    def suction_command_callback(self, msg):
        """ROS 2 명령을 받아 ESP32로 전송"""
        command = msg.data
        if command in ['Suction ON', 'Suction OFF']:
            self.client.send(command.encode())  # ESP32로 명령 전송
            response = self.client.recv(1024).decode()  # ESP32 응답 수신
            self.get_logger().info(f"ESP32 response: {response}")

            # ROS2 토픽으로 응답 발행
            msg = String()
            msg.data = response
            self.publisher.publish(msg)
        else:
            self.get_logger().warn("유효하지 않은 명령입니다.")

    def close_server(self):
        """서버 종료"""
        self.client.close()
        self.server.close()
        self.get_logger().info("Server closed.")

def main(args=None):
    rclpy.init(args=args)
    node = SuctionControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Suction Control Node 종료...")
    finally:
        node.close_server()
        node.destroy_node()
        rclpy.shutdown()
