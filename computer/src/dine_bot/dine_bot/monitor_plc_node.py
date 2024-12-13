import rclpy
from rclpy.node import Node
from pymodbus.client import ModbusSerialClient
from std_msgs.msg import String
import threading
import time


class PLCControlNode(Node):
    def __init__(self):
        super().__init__('plc_control_node')

        # Modbus 클라이언트 설정
        self.client = ModbusSerialClient(
            port='/dev/ttyUSB0',  # PLC가 연결된 직렬 포트
            baudrate=19200,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )

        # Modbus 주소 설정
        self.m0_address = 0
        self.m1_address = 1
        self.m2_address = 2

        # 이전 상태 저장 변수
        self.previous_states = {self.m1_address: None, self.m2_address: None}

        # mycobot에서 주문 들어올 때 동작
        self.subscription = self.create_subscription(
            String,
            'plc_control',
            self.listener_order,
            10
        )

        # ROS 2 Publisher 설정
        self.esp32_publisher = self.create_publisher(String, 'esp32_control', 10)
        self.robot_publisher = self.create_publisher(String, 'robot_control', 10)

        # PLC 연결
        if self.client.connect():
            self.get_logger().info("PLC 연결 성공")
            threading.Thread(target=self.monitor_plc_states, daemon=True).start()
        else:
            self.get_logger().error("PLC 연결 실패")
            self.destroy_node()

    def listener_order(self, msg):
        """주문 받으면 처리."""
        menu_name = msg.data
        try:
            # 추후 로직 다르게 작성
            # if menu_name == "salad": 
            self.set_m0_value(1)
            self.send_esp32_command("1번 디스펜서 작동")
            # else:
            #     self.get_logger().info("알 수 없는 입력입니다.")
        except Exception as e:
            self.get_logger().error(f"[에러] 입력 처리 중 문제 발생: {e}")

    def set_m0_value(self, value):
        """M0 값 설정."""
        try:
            response = self.client.write_coil(self.m0_address, value, unit=1)
            if response.isError():
                self.get_logger().error(f"[에러] M0 값 설정 실패: {response}")
            else:
                self.get_logger().info(f"M0 값 {value}로 설정 완료")
        except Exception as e:
            self.get_logger().error(f"[에러] M0 설정 중 문제 발생: {e}")

    def monitor_plc_states(self):
        """M1과 M2 상태를 모니터링."""
        while rclpy.ok():
            try:
                response = self.client.read_coils(self.m1_address, 2, unit=1)  # M1부터 2개의 Coil 읽기
                if response.isError():
                    self.get_logger().error(f"[에러] M1/M2 읽기 실패: {response}")
                else:
                    current_states = {
                        self.m1_address: response.bits[0],  # M1 상태
                        self.m2_address: response.bits[1]  # M2 상태
                    }

                    # 상태 변경 확인 및 처리
                    for address, current_state in current_states.items():
                        previous_state = self.previous_states[address]
                        if previous_state is not None and previous_state != current_state:
                            if address == self.m1_address and current_state == 1:
                                self.send_esp32_command("2번 디스펜서 작동")
                            elif address == self.m2_address and current_state == 1:
                                self.send_robot_command("재료 준비 완료")

                        # 상태 업데이트
                        self.previous_states[address] = current_state

            except Exception as e:
                self.get_logger().error(f"[에러] M1/M2 읽기 중 문제 발생: {e}")

            time.sleep(1)  # 1초 주기

    def send_esp32_command(self, command):
        """ESP32 제어 명령 전송."""
        msg = String()
        msg.data = command
        self.esp32_publisher.publish(msg)
        self.get_logger().info(f"ESP32 제어 명령 전송: {command}")

    def send_robot_command(self, command):
        """로봇암 제어 명령 전송."""
        msg = String()
        msg.data = command
        self.robot_publisher.publish(msg)
        self.get_logger().info(f"로봇암 제어 명령 전송: {command}")

    def destroy_node(self):
        """노드 종료 시 클라이언트 연결 해제."""
        self.client.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = PLCControlNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
