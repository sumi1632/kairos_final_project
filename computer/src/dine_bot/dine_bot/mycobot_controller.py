import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from custom_msgs.action import Cook
from std_msgs.msg import String
from pymycobot.mycobot import MyCobot
import time
from collections import deque
import threading

class CookActionServer(Node):
    def __init__(self):
        super().__init__('mycobot_controller')
        self._action_server = ActionServer(
            self,
            Cook,
            'start_cook',
            execute_callback=self.execute_callback
        )
        self.goal_handle = None

        self.get_logger().info('mycobot_controller is ready.')

        # ROS 2 Subscriber 및 Publisher 설정
        self.subscription = self.create_subscription(String, 'robot_control', self.plc_callback, 10)
        self.plc_publisher = self.create_publisher(String, 'plc_control', 10)
        self.suction_publisher = self.create_publisher(String, 'suction_command', 10)

        # 로봇 초기화
        try:
            self.mycobot = MyCobot('/dev/ttyACM0', 115200)
            self.get_logger().info("Robot Control Node Initialized")
            self.initialize_robot()
        except Exception as e:
            self.get_logger().error(f"로봇 초기화 중 오류 발생: {e}")
            raise e

        self.is_ready_for_robotarm_move = False

        # 주문 관리
        self.orders = deque()
        self.is_cooking = False
        self.current_menu = ""
        self.cooking_done_event = threading.Event()

    def initialize_robot(self):
        """로봇 초기화"""
        try:
            self.mycobot.set_gripper_mode(0)
            self.mycobot.init_eletric_gripper()
            self.mycobot.set_gripper_state(0, 50)
            self.mycobot.send_angles([0, 0, 0, 0, 0, 0], 30)
            time.sleep(2)
            self.get_logger().info("로봇 초기화 완료")
        except Exception as e:
            self.get_logger().error(f"로봇 초기화 단계에서 오류 발생: {e}")
            raise e

    async def execute_callback(self, goal_handle):
        """액션 서버의 메인 콜백"""
        self.goal_handle = goal_handle
        menu_name = goal_handle.request.menu_name
        self.orders.append(menu_name)
        self.get_logger().info(f'Received cooking request for: {menu_name}')

        if not self.is_cooking:
            self.cooking_done_event.clear()

            thread = threading.Thread(target=self.start_cook)
            thread.start()

            while not self.cooking_done_event.is_set():
                time.sleep(1)

            # 결과 반환
            result = Cook.Result()
            result.cook_result = f'Cooking for {menu_name} is completed!'
            goal_handle.succeed()
            self.get_logger().info(result.cook_result)
            return result

    def start_cook(self):
        """요리 시작"""
        self.is_cooking = True
        try:
            self.current_menu = self.orders.popleft()
            self.get_logger().info(f'Starting to cook: {self.current_menu}')

            # PLC 동작 시작 알림
            plc_msg = String()
            plc_msg.data = f"Start cooking: {self.current_menu}"
            self.plc_publisher.publish(plc_msg)
            self.get_logger().info("PLC에 요리 시작 알림 전송")

            # 로봇 암이 이동할 준비가 될 때까지 대기
            self.get_logger().info("로봇 암 이동 준비 대기 중...")
            wait_start_time = time.time()
            timeout = 60  # 예: 60초 타임아웃
            while not self.is_ready_for_robotarm_move:
                if time.time() - wait_start_time > timeout:
                    self.get_logger().error("로봇 암 이동 준비 타임아웃")
                    self.complete_task()
                    return
                time.sleep(1)

            self.is_ready_for_robotarm_move = False

            # 작업 수행
            self.send_feedback("Preparing")
            self.material_handling()
            self.send_feedback("Cooking")
            self.liquid_dispensing()
            self.cooking_tool_handling()
            self.send_feedback("Plating")
            self.suction_cup_handling()

            self.get_logger().info("Suction cup handling 완료, 이제 fan_handling을 시작합니다.")
            self.fan_handling()
            self.get_logger().info("fan_handling 완료")

        except Exception as e:
            self.get_logger().error(f"요리 과정 중 오류 발생: {e}")
        finally:
            self.complete_task()

    def send_feedback(self, status):
        """피드백 전송"""
        if self.goal_handle:
            try:
                feedback_msg = Cook.Feedback()
                feedback_msg.cook_status = status
                self.goal_handle.publish_feedback(feedback_msg)
                self.get_logger().info(f'Feedback: {status}')
            except Exception as e:
                self.get_logger().error(f"피드백 전송 중 오류 발생: {e}")

    def plc_callback(self, msg):
        """PLC 명령 수신"""
        command = msg.data
        if command in ["작업 시작", "재료 준비 완료"]:
            self.get_logger().info(f"명령 수신: {command}")
            self.is_ready_for_robotarm_move = True
        else:
            self.get_logger().warn(f"알 수 없는 명령: {command}")
    def suction_command_callback(self, command: str):
        """
        흡착 컵 명령을 suction_cup_node로 전송
        :param command: "Suction ON" 또는 "Suction OFF"
        """
        try:
            # 명령 유효성 확인
            if command not in ["Suction ON", "Suction OFF"]:
                self.get_logger().warn(f"유효하지 않은 석션 명령: {command}")
                return
            
            # 메시지 생성 및 발행
            suction_msg = String()
            suction_msg.data = command
            self.suction_publisher.publish(suction_msg)
            self.get_logger().info(f"{command} 명령 suction_cup_node로 전송 완료")
        except Exception as e:
            self.get_logger().error(f"suction_command_callback 중 오류 발생: {e}")

    def material_handling(self):
        """재료 이동 및 준비"""
        try:
            self.get_logger().info("재료 이동 및 준비 단계 시작")
            self.get_logger().info("첫 번째 위치로 이동")
            self.mycobot.send_angles([89.64, 0.7, 4.3, -5.0, -91.14, -4.57], 30)
            time.sleep(5)

            # self.get_logger().info("재료 잡기 위치로 이동")
            # self.mycobot.send_angles([88.85, 28.65, 54.49, -60.99, -89.91, -0.61], 30)
            # time.sleep(5)

            # self.get_logger().info("재료 잡기 위치로 깊숙히 이동")
            # self.mycobot.send_angles([86.83, 40.07, 47.54, -65.56, -85.69, -1.49], 30)
            # time.sleep(5)

            # self.get_logger().info("그리퍼로 재료 잡기")
            # self.mycobot.set_gripper_state(1, 100)
            # time.sleep(4)

            # self.get_logger().info("재료 잡기 위치로 이동2")
            # self.mycobot.send_angles([88.85, 28.65, 54.49, -60.99, -89.91, -0.61], 30)
            # time.sleep(5)

            # self.get_logger().info("재료 들어올리기")
            # self.mycobot.send_angles([88.15, -31.46, 98.87, -47.98, -86.74, -0.79], 30)
            # time.sleep(5)

            # self.get_logger().info("이동 경로 1")
            # self.mycobot.send_angles([154.95, -15.38, 103.27, -50.88, -79.45, -0.17], 30)
            # time.sleep(5)

            # self.get_logger().info("이동 경로 2")
            # self.mycobot.send_angles([154.95, -15.38, 103.27, -63, -79.45, 130], 20)
            # time.sleep(5)

            # self.get_logger().info("이동 경로 3")
            # self.mycobot.send_angles([154.86, -51.06, 96.59, -23.9, -80.77, 0], 30)
            # time.sleep(5)

            # self.get_logger().info("중간 위치 조정")
            # self.mycobot.send_angles([-90, 0, 0, 0, 90, 0], 30)
            # time.sleep(5)

            # self.get_logger().info("재료 내리기 중간 위치로 이동")
            # self.mycobot.send_angles([-90, 0, 0, 0, 45, 0], 30)
            # time.sleep(5)

            # self.get_logger().info("재료 내려놓기 자세")
            # self.mycobot.send_angles([-80.85, -79.1, 63.89, 23.9, 39.55, -6.94], 30)
            # time.sleep(5)

            # self.get_logger().info("그리퍼 열어서 재료 내려놓기")
            # self.mycobot.set_gripper_state(0, 100)
            # time.sleep(4)

            self.get_logger().info("위치 조정")
            self.mycobot.send_angles([-89.38, -17.24, -5.97, 31.72, 54.75, 0.7], 30)
            time.sleep(5)

            self.get_logger().info("재료 준비 완료")
        except Exception as e:
            self.get_logger().error(f"material_handling 중 오류 발생: {e}")
            raise e

    def liquid_dispensing(self):
        """액체 디스펜서 동작"""
        try:
            self.get_logger().info("\n=== 액체 디스펜서 동작 단계 시작 ===")
            self.get_logger().info("팬 위치로 이동")
            self.mycobot.send_angles([3.86, -23.37, -34.01, -22.5, 88.5, 1.75], 30)
            time.sleep(5)

            # self.get_logger().info("팬 잡기 위치")
            # self.mycobot.send_angles([1.75, -36.38, -38.05, -14.23, 90.79, 1.84], 30)
            # time.sleep(5)

            # self.get_logger().info("팬 잡기")
            # self.mycobot.set_gripper_state(1, 100)
            # time.sleep(4)

            # self.get_logger().info("팬 들어올리기")
            # self.mycobot.send_angles([-0.08, -23.55, -44.29, -18.1, 97.55, 0.26], 30)
            # time.sleep(5)

            # self.get_logger().info("디스펜서 위치 1")
            # self.mycobot.send_angles([-10.98, -45.86, 8.61, -41.74, 90.87, 13.97], 30)
            # time.sleep(5)

            # self.get_logger().info("디스펜서 위치 2")
            # self.mycobot.send_angles([3.77, -51.41, -1.05, -38.58, 91.23, 1.23], 30)
            # time.sleep(5)

            # self.get_logger().info("디스펜서 내려놓기")
            # self.mycobot.set_gripper_state(0, 100)
            # time.sleep(4)

            self.get_logger().info("초기 위치로 복귀")
            self.mycobot.send_angles([0, 0, 0, 0, 0, 0], 30)
            time.sleep(5)

            self.get_logger().info("액체 디스펜서 동작 완료")
        except Exception as e:
            self.get_logger().error(f"liquid_dispensing 중 오류 발생: {e}")
            raise e

    def cooking_tool_handling(self):
        """조리도구 동작"""
        try:
            self.get_logger().info("\n=== 조리도구 동작 단계 시작 ===")
            self.get_logger().info("조리도구 위치로 이동")
            self.mycobot.send_angles([0, 0, 0, 0, 107, 0], 30)
            time.sleep(5)

            self.get_logger().info("조리도구 잡기 위치")
            self.mycobot.send_angles([-9.5, -57.65, -36.05, 102.26, 107.31, 1.4], 30)
            time.sleep(5)

            self.get_logger().info("조리도구 잡기")
            self.mycobot.set_gripper_state(1, 100)
            time.sleep(4)

            self.get_logger().info("조리도구 들어올리기")
            self.mycobot.send_angles([-9, -14.06, -99.75, 108.1, 107.92, 0.7], 30)
            time.sleep(5)

            # 젓기 동작 시작
            stir_angles = [
                [-10, -32.43, -99.75, 132, 113, 3],
                [-10, -32.43, -99.75, 132, 113, -20],
                [-10, -32.43, -99.75, 132, 113, 3],
                [-10, -32.43, -99.75, 132, 113, -20],
                [-10, -32.43, -99.75, 132, 113, 3]
            ]
            for idx, angles in enumerate(stir_angles, 1):
                self.get_logger().info(f"젓기 동작 {idx}/5")
                self.mycobot.send_angles(angles, 30)
                time.sleep(2)

            self.get_logger().info("조리도구 회수 시작")
            self.mycobot.send_angles([-9, -14.06, -99.75, 108.1, 107.92, 0.7], 30)
            time.sleep(5)

            self.get_logger().info("조리도구 되걸기 중간 위치")
            self.mycobot.send_angles([-10, -66.65, -23.55, 105.26, 107.31, 1.4], 30)
            time.sleep(5)

            self.get_logger().info("조리도구 되걸기")
            self.mycobot.send_angles([-10, -66.65, -23.55, 102.26, 107.31, 1.4], 30)
            time.sleep(5)

            self.get_logger().info("조리도구 내려놓기")
            self.mycobot.set_gripper_state(0, 100)
            time.sleep(4)
            
            self.get_logger().info("빠지기")
            self.mycobot.send_angles([-9, -46.65, -33.55, 102.26, 107.31, 1.4], 30)
            time.sleep(5)

            self.get_logger().info(">>> 조리도구 동작 완료\n")
        except Exception as e:
            self.get_logger().error(f"cooking_tool_handling 중 오류 발생: {e}")
            raise e

    def suction_cup_handling(self):
        """흡착 컵 동작"""
        try:
            self.get_logger().info("석션 준비 자세")
            self.mycobot.send_angles([-61.52, 55.98, -9.75, -42.09, -15.11, -9.66], 30)
            time.sleep(5)

            self.get_logger().info("석션 잡기 준비")
            self.mycobot.send_angles([-50.71, 99, -20.56, -70.66, -20.03, -12.74], 30)
            time.sleep(5)

            self.mycobot.set_gripper_state(1, 100)
            self.get_logger().info("그리퍼로 석션 잡기")
            time.sleep(4)

            self.get_logger().info("석션 들어 올림")
            self.mycobot.send_angles([-49.13, 85.51, -14.67, -63.28, -27.77, -10.1], 30)
            time.sleep(5)

            self.get_logger().info("석션 접시 위 위치함")
            self.mycobot.send_angles([-42.53, 86.04, -7.55, -68.55, 5.8, -12.74], 30)
            time.sleep(20)

            self.get_logger().info("석션 위해 접시로 접근")
            self.mycobot.send_angles([-43.5, 88.15, 18.8, -101.6, 5.36, -15.29], 30)
            time.sleep(9)

            self.suction_command_callback("Suction ON")
            time.sleep(5)

            self.get_logger().info("석션 위해 접시로 접근")
            self.mycobot.send_angles([-45.0, 46.58, 24.16, -64.68, -3.33, -11.42], 30)
            time.sleep(5)

            self.get_logger().info("접시 들어 올림")
            self.mycobot.send_angles([-81.73, 69.34, -12.12, -55.72, -52.29, 0.08], 30)
            time.sleep(5)

            self.get_logger().info("AGV 위에 접시 올림")
            self.mycobot.send_angles([-82.35, 83.23, 3.07, -81.82, -54.66, -4.04], 30)
            time.sleep(15)

            self.suction_command_callback("Suction OFF")
            time.sleep(5)

            self.get_logger().info("접시 놓은 후 웨이 포인트")
            self.mycobot.send_angles([-82.17, 57.74, -14.15, -41.3, -46.14, 1.23], 30)
            time.sleep(5)

            self.get_logger().info("석션 내려놓기 중간 위치")
            self.mycobot.send_angles([-51.59, 94.83, -17.22, -29.35, 5.53, -51.41], 30)
            time.sleep(5)

            self.get_logger().info("석션 내려 놓음")
            self.mycobot.send_angles([-50.71, 99, -20.56, -70.66, -20.03, -12.74], 30)
            time.sleep(5)

            self.get_logger().info("그리퍼 열기")
            self.mycobot.set_gripper_state(0, 100)
            time.sleep(4)

            self.get_logger().info("석션 내려 놓고 위치 조정1")
            self.mycobot.send_angles([-60.71, 99, -20.56, -70.66, -20.03, -12.74], 30)
            time.sleep(5)

            self.get_logger().info("석션 내려 놓고 위치 조정1")
            self.mycobot.send_angles([-55.8, 60.98, -17.05, -28.12, 5.97, -60.73], 30)
            time.sleep(5)

            self.get_logger().info("흡착 컵 동작 완료")
        except Exception as e:
            self.get_logger().error(f"suction_cup_handling 중 오류 발생: {e}")
            raise e

    def fan_handling(self):
        """조리 완료된 음식 담기"""
        try:
            self.get_logger().info("팬 다시 잡기 웨이 포인트1")
            self.mycobot.send_angles([-5.18, -6.32, 10.45, 2.1, -87.53, 6.5], 30)
            time.sleep(5)

            self.get_logger().info("팬 다시 잡기 웨이 포인트2")
            self.mycobot.send_angles([-2.54, -15.9, 19.59, 5.62, 93.6, 6.15], 30)
            time.sleep(5)

            self.get_logger().info("팬 잡기 위치")
            self.mycobot.send_angles([3.77, -51.41, -1.05, -38.58, 91.23, 1.23], 30)
            time.sleep(5)

            self.get_logger().info("그리퍼 닫기")
            self.mycobot.set_gripper_state(1, 100)  # 그리퍼 닫기
            time.sleep(4)

            self.get_logger().info("팬 들어 올림")
            self.mycobot.send_angles([45, -51.41, -1.05, -38.58, 91.23, 1.23], 30)
            time.sleep(5)

            self.get_logger().info("AGV 위 접시로 접근")
            self.mycobot.send_angles([144.66, -29.88, -1.4, -11.51, 65.03, -16.17], 30)
            time.sleep(5)

            self.get_logger().info("쏟기 1")
            self.mycobot.send_angles([144.75, -45.43, 37.0, -20.3, 58.71, -37.17], 30)
            time.sleep(5)

            self.get_logger().info("쏟기 2")
            self.mycobot.send_angles([158.55, -66.5, 13.79, -27.68, -31.64, -33.66], 30)
            time.sleep(5)
            
            self.get_logger().info("쏟기 3")
            self.mycobot.send_angles([158.9, -4.21, 25.4, -26.19, 17.13, -13.27], 30)
            time.sleep(5)

            self.get_logger().info("쏟고 들어 올리기")
            self.mycobot.send_angles([130.16, -2.98, -2.54, -49.21, 92.1, -19.86], 30)
            time.sleep(5)

            self.get_logger().info("팬 원위치 웨이 포인트")
            self.mycobot.send_angles([1.75, 1.23, 1.23, -44.2, 86.57, -17.22], 30)
            time.sleep(5)

            self.get_logger().info("팬 내려놓기 위치")
            self.mycobot.send_angles([3.77, -51.41, -1.05, -38.58, 91.23, 1.23], 30)
            time.sleep(5)

            self.get_logger().info("그리퍼 열기")
            self.mycobot.set_gripper_state(0, 100)  # 그리퍼 열기
            time.sleep(4)

            self.get_logger().info("조리 완료된 음식 담기 동작 완료")
        except Exception as e:
            self.get_logger().error(f"fan_handling 중 오류 발생: {e}")
            raise e

    def complete_task(self):
        """작업 완료 처리"""
        try:
            self.get_logger().info("작업 완료 처리 시작")
            self.mycobot.send_angles([0, 0, 0, 0, 0, 0], 20)
            time.sleep(3)
            self.get_logger().info("작업 완료 및 초기화 위치 복귀")
            self.is_cooking = False
            self.cooking_done_event.set()
        except Exception as e:
            self.get_logger().error(f"complete_task 중 오류 발생: {e}")

def main(args=None):
    rclpy.init(args=args)
    cook_action_server = CookActionServer()

    executor = MultiThreadedExecutor(num_threads=2)

    try:
        rclpy.spin(cook_action_server, executor=executor)
    except KeyboardInterrupt:
        cook_action_server.get_logger().info('Cook Action Server shutting down.')
    finally:
        cook_action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
