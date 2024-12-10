import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket
import time


class ESP32ControlNode(Node):
    def __init__(self):
        super().__init__('esp32_control_node')

        # ROS 2 Subscriber 설정
        self.subscription = self.create_subscription(
            String,
            'esp32_control',
            self.listener_callback,
            10
        )

        # 소켓 서버 설정
        self.server_ip = '0.0.0.0'
        self.server_port = 10000

        self.get_logger().info("Starting ESP32 server...")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.server_ip, self.server_port))
        self.server.listen(1)
        self.get_logger().info(f"Server listening on {self.server_ip}:{self.server_port}")

        self.client = None
        self.addr = None
        self.wait_for_connection()

    def wait_for_connection(self):
        """ESP32와의 연결을 기다립니다."""
        while True:
            try:
                self.get_logger().info("Waiting for connection...")
                self.client, self.addr = self.server.accept()
                self.get_logger().info(f"Connection established with {self.addr}")
                break
            except socket.error as e:
                self.get_logger().error(f"Socket error while waiting for connection: {e}")
                time.sleep(1)
            except KeyboardInterrupt:
                self.get_logger().info("Server interrupted.")
                self.cleanup()
                raise
            except Exception as e:
                self.get_logger().error(f"Unexpected error while waiting for connection: {e}")
                time.sleep(1)

    def listener_callback(self, msg):
        """ROS 2 토픽에서 명령을 수신하고 처리."""
        command = msg.data
        self.get_logger().info(f"Received command from PLC Node: {command}")

        if command == "1번 디스펜서 작동":
            self.execute_motor_command('3')  # 1번 디스펜서 모터 동작 명령어: '3'
        elif command == "2번 디스펜서 작동":
            self.execute_motor_command('1')  # 2번 디스펜서 모터 동작 명령어: '1'
        else:
            self.get_logger().warn(f"Unknown command received: {command}")

    def execute_motor_command(self, motor_command):
        """모터 명령을 ESP32로 전송하고 4번 반복."""
        try:
            for i in range(4):
                if self.client is None:
                    self.get_logger().error("Client is not connected.")
                    break
                self.client.send(motor_command.encode())
                self.get_logger().info(f"Sent command to ESP32: {motor_command}")
                response = self.client.recv(1024).decode()
                self.get_logger().info(f"ESP32 response: {response}")
                time.sleep(1)
        except socket.error as e:
            self.get_logger().error(f"Socket error during motor execution: {e}")
            self.cleanup()
        except Exception as e:
            self.get_logger().error(f"Unexpected error during motor execution: {e}")

    def cleanup(self):
        """자원 정리."""
        if self.client:
            self.client.close()
            self.client = None
        if self.server:
            self.server.close()
            self.server = None
        self.get_logger().info("Cleaned up sockets.")


def main(args=None):
    rclpy.init(args=args)
    node = ESP32ControlNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("ESP32 Control Node shutting down...")
    finally:
        node.cleanup()
        rclpy.shutdown()
        node.destroy_node()


if __name__ == '__main__':
    main()
