import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket

class SuctionCupNode(Node):
    def __init__(self):
        super().__init__('suction_cup_node')

        # ROS 2 Subscriber 및 Publisher 설정
        self.subscription = self.create_subscription(
            String, 'suction_command', self.suction_command_callback, 10)
        self.publisher = self.create_publisher(String, 'suction_response', 10)

        # 소켓 설정
        self.server_ip = "172.30.1.86"  # ESP32 IP 주소
        self.server_port = 8882
        self.client = None
        self.connect_to_esp32()

    def connect_to_esp32(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server_ip, self.server_port))
            self.get_logger().info(f"Connected to ESP32 at {self.server_ip}:{self.server_port}")
        except Exception as e:
            self.get_logger().error(f"Failed to connect to ESP32: {e}")

    def suction_command_callback(self, msg):
        """ROS 2 명령을 받아 ESP32로 전송"""
        command = msg.data.strip()
        if command not in ["Suction ON", "Suction OFF"]:
            self.get_logger().warn(f"Invalid suction command: {command}")
            return

        try:
            self.client.sendall((command + '\n').encode())
            response = self.client.recv(1024).decode().strip()
            self.get_logger().info(f"ESP32 Response: {response}")

            # 응답 발행
            response_msg = String()
            response_msg.data = response
            self.publisher.publish(response_msg)
        except Exception as e:
            self.get_logger().error(f"Error communicating with ESP32: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SuctionCupNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down suction_cup_node...")
    finally:
        if node.client:
            node.client.close()
        node.destroy_node()
        rclpy.shutdown()
