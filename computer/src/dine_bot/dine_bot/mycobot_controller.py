import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from custom_msgs.action import Cook
from std_msgs.msg import String
from pymycobot.mycobot import MyCobot
import time
from collections import deque

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
        self.mycobot = MyCobot('/dev/ttyACM0', 115200)
        self.get_logger().info("Robot Control Node Initialized")
        self.initialize_robot()

        # 주문 관리
        self.orders = deque()
        self.is_cooking = False
        self.current_menu = ""

    def initialize_robot(self):
        """로봇 초기화"""
        self.mycobot.set_gripper_mode(0)
        self.mycobot.init_eletric_gripper()
        self.mycobot.set_gripper_state(0, 50)
        self.mycobot.send_angles([0, 0, 0, 0, 0, 0], 100)
        time.sleep(2)
        self.get_logger().info("로봇 초기화 완료")

    async def execute_callback(self, goal_handle):
        # 주문 접수
        self.goal_handle = goal_handle
        menu_name = goal_handle.request.menu_name
        self.orders.append(menu_name)
        self.get_logger().info(f'Received cooking request for: {menu_name}')
        start_cook()
    
    def start_cook(self):
        if self.is_cooking == False:
            self.is_cooking = True
            self.current_menu = self.orders.popleft()
            self.get_logger().info(f'Cooking : {self.current_menu}')

            # plc 동작
            self.plc_publisher.publish(self.current_menu)
        else:
            self.get_logger().info(f'The first received dish is being cooked')

    def plc_callback(self, msg):
        """plc 수신 및 작업 시작"""
        command = msg.data
        if command == "작업 시작" or command == "재료 준비 완료":
            self.get_logger().info(f"명령 수신: {command}")
            self.execute_task()
        else:
            self.get_logger().warn(f"알 수 없는 명령: {command}")

    def execute_task(self):
        """작업 순서대로 수행"""
        self.send_feedback("Preparing")
        self.material_handling()           # 재료 이동 및 준비
        self.send_feedback("Cooking")
        self.cooking_tool_handling()       # 조리도구 동작
        self.liquid_dispensing()           # 액체 디스펜서 동작
        self.send_feedback("Plating")
        self.suction_cup_handling()        # 흡착 컵 동작
        self.complete_task()

    def send_feedback(self, msg):
        feedback_msg = Cook.Feedback()
        feedback_msg.cook_status = msg
        self.get_logger().info(f'Feedback: {msg}')
        self.goal_handle.publish_feedback(feedback_msg)

    def material_handling(self):
        """재료 이동 및 준비"""
        self.get_logger().info("첫 번째 위치로 이동")
        self.mycobot.send_angles([89.64, 0.7, 4.3, -5.0, -91.14, -4.57], 30)
        time.sleep(5)
        self.get_logger().info("재료 잡기 위치로 이동")
        self.mycobot.send_angles([88.85, 28.65, 54.49, -60.99, -89.91, -0.61], 30)
        time.sleep(5)
        self.get_logger().info("재료 잡기 위치로 깊숙히 이동")
        self.mycobot.send_angles([86.83, 40.07, 47.54, -65.56, -85.69, -1.49], 30)
        time.sleep(5)
        self.get_logger().info("그리퍼로 재료 잡기")
        self.mycobot.set_gripper_state(1, 100)
        time.sleep(4)
        self.get_logger().info("재료 잡기 위치로 이동2")
        self.mycobot.send_angles([88.85, 28.65, 54.49, -60.99, -89.91, -0.61], 30)
        time.sleep(5)
        self.get_logger().info("재료 들어올리기")
        self.mycobot.send_angles([88.15, -31.46, 98.87, -47.98, -86.74, -0.79], 30)
        time.sleep(5)
        self.get_logger().info("이동 경로 1")
        self.mycobot.send_angles([154.95, -15.38, 103.27, -50.88, -79.45, -0.17], 30)
        time.sleep(5)
        self.get_logger().info("이동 경로 2")
        self.mycobot.send_angles([154.95, -15.38, 103.27, -63, -79.45, 150], 20)
        time.sleep(5)
        self.get_logger().info("이동 경로 3")
        self.mycobot.send_angles([154.86, -51.06, 96.59, -23.9, -80.77, 0], 30)
        time.sleep(5)
        self.get_logger().info("중간 위치 조정")
        self.mycobot.send_angles([-90, 0, 0, 0, 90, 0], 30)
        time.sleep(5)
        self.get_logger().info("재료 내리기 중간 위치로 이동")
        self.mycobot.send_angles([-90, 0, 0, 0, 45, 0], 30)
        time.sleep(5)
        self.get_logger().info("재료 내려놓기 자세")
        self.mycobot.send_angles([-80.85, -79.1, 63.89, 23.9, 39.55, -6.94], 30)
        time.sleep(5)
        self.get_logger().info("그리퍼 열어서 재료 내려놓기")
        self.mycobot.set_gripper_state(0, 100)
        time.sleep(4)
        self.get_logger().info("위치 조정")
        self.mycobot.send_angles([-89.38, -27.24, -5.97, 31.72, 54.75, 0.7], 30)
        time.sleep(5)
        self.get_logger().info("재료 준비 완료")

    def cooking_tool_handling(self):
        self.get_logger().info("\n=== 조리도구 동작 단계 시작 ===")
        self.get_logger().info("조리도구 위치로 이동")
        self.mycobot.send_angles([0, 0, 0, 0, 107, 0], 30)
        time.sleep(5)
        self.get_logger().info("조리도구 잡기 위치")
        self.mycobot.send_angles([-10.1, -57.65, -36.05, 102.26, 107.31, 1.4], 30)
        time.sleep(5)
        self.get_logger().info("조리도구 잡기")
        self.mycobot.set_gripper_state(1, 100)
        time.sleep(4)
        self.get_logger().info("조리도구 들어올리기")
        self.mycobot.send_angles([-13.97, -14.06, -99.75, 108.1, 107.92, 0.7], 30)
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
        self.mycobot.send_angles([-8, -22, -99.75, 132, 100, 6], 30)
        time.sleep(5)
        self.get_logger().info("조리도구 되돌리기")
        self.mycobot.send_angles([-55, -22, -99.75, 132, 100, 6], 30)
        time.sleep(5)
        self.get_logger().info("조리도구 내려놓기")
        self.mycobot.set_gripper_state(0, 100)
        time.sleep(4)
        self.get_logger().info(">>> 조리도구 동작 완료\n")

    def liquid_dispensing(self):
        """액체 디스펜서 동작"""
        self.get_logger().info("\n=== 액체 디스펜서 동작 단계 시작 ===")
        self.get_logger().info("팬 위치로 이동")
        self.mycobot.send_angles([3.86, -23.37, -34.01, -22.5, 88.5, 1.75], 30)
        time.sleep(5)
        self.get_logger().info("팬 잡기 위치")
        self.mycobot.send_angles([1.75, -36.38, -38.05, -14.23, 90.79, 1.84], 30)
        time.sleep(5)
        self.get_logger().info("팬 잡기")
        self.mycobot.set_gripper_state(1, 100)
        time.sleep(4)
        self.get_logger().info("팬 들어올리기")
        self.mycobot.send_angles([-0.08, -23.55, -44.29, -18.1, 97.55, 0.26], 30)
        time.sleep(5)
        self.get_logger().info("디스펜서 위치 1")
        self.mycobot.send_angles([-10.98, -45.86, 8.61, -41.74, 90.87, 13.97], 30)
        time.sleep(5)
        self.get_logger().info("디스펜서 위치 2")
        self.mycobot.send_angles([3.77, -51.41, -1.05, -38.58, 91.23, 1.23], 30)
        time.sleep(5)
        self.get_logger().info("디스펜서 내려놓기")
        self.mycobot.set_gripper_state(0, 100)
        time.sleep(4)
        self.get_logger().info("초기 위치로 복귀")
        self.mycobot.send_angles([0, 0, 0, 0, 0, 0], 30)
        time.sleep(5)
        self.get_logger().info("액체 디스펜서 동작 완료")

    def suction_cup_handling(self):
        """흡착 컵 동작"""
        self.get_logger().info("흡착 컵 동작 시작")
        self.mycobot.send_angles([-6.5, 58.27, -45.61, -16.25, -32.16, -7.11], 30)
        time.sleep(5)
        self.mycobot.send_angles([3.25, 69.16, -42.18, -23.46, -36.56, -7.03], 30)
        time.sleep(5)
        self.mycobot.set_gripper_state(1, 100)
        time.sleep(4)
        self.mycobot.send_angles([-6.5, 58.27, -45.61, -16.25, -32.16, -7.11], 30)
        time.sleep(5)
        self.mycobot.send_angles([-80.06, 71.01, -54.66, -7.29, 17.13, 11.07], 30)
        time.sleep(5)
        self.mycobot.send_angles([-60.38, 111.7, -39.11, -91.05, 17.13, 11.07], 30)
        time.sleep(5)
        suction_on_msg = String()
        suction_on_msg.data = "Suction ON"
        self.suction_publisher.publish(suction_on_msg)
        self.get_logger().info("Suction ON 명령 suction_cup_node로 전송")
        self.mycobot.send_angles([-71.38, 77, -61, -21, 19, 0], 30)
        time.sleep(5)
        self.mycobot.send_angles([-150, 77, -61, -21, 19, 0], 30)
        time.sleep(5)
        self.mycobot.send_angles([-150, 77, 7, -86, 19, 0], 30)
        time.sleep(5)
        suction_off_msg = String()
        suction_off_msg.data = "Suction OFF"
        self.suction_publisher.publish(suction_off_msg)
        self.get_logger().info("Suction OFF 명령 suction_cup_node로 전송")
        self.mycobot.send_angles([-150, 77, -61, -21, 19, 0], 30)
        time.sleep(5)
        self.mycobot.send_angles([-6.5, 58.27, -45.61, -16.25, -32.16, -7.11], 30)
        time.sleep(5)
        self.mycobot.send_angles([3.25, 69.16, -55, -23.46, -36.56, -6], 30)
        time.sleep(5)
        self.mycobot.set_gripper_state(0, 100)
        time.sleep(4)
        self.get_logger().info("흡착 컵 동작 완료")

    def complete_task(self):
        """작업 완료"""
        self.mycobot.send_angles([0, 0, 0, 0, 0, 0], 20)
        time.sleep(3)
        self.get_logger().info("작업 완료 및 초기화 위치 복귀")
        self.is_cooking = False

        # Cooking complete
        result = Cook.Result()
        result.cook_result = f'Cooking for {self.current_menu} is completed!'
        self.get_logger().info(result.cook_result)
        self.goal_handle.succeed()

        # 다음 주문 있으면 요리
        if len(self.orders) > 0:
            start_cook()

def main(args=None):
    rclpy.init(args=args)
    cook_action_server = CookActionServer()
    try:
        rclpy.spin(cook_action_server)
    except KeyboardInterrupt:
        cook_action_server.get_logger().info('Cook Action Server shutting down.')
    finally:
        cook_action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()