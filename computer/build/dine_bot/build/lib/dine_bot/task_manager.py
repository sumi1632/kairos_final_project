import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from custom_msgs.action import Cook, Serve
from custom_msgs.srv import ReceiveOrder
from custom_msgs.msg import UpdateStatus
from std_msgs.msg import String
from queue import Queue
import socket
import threading


class TaskManager(Node):
    def __init__(self):
        super().__init__('task_manager_node')

        self.start_cook_client = ActionClient(self, Cook, 'start_cook')

        self.receive_order_client = self.create_client(ReceiveOrder, 'receive_order')

        self.start_serve_client = ActionClient(self, Serve, 'start_serve')

        self.cook_status_publisher = self.create_publisher(
            UpdateStatus,
            '/update_cook_status',
            10)

        self.order_status_publisher = self.create_publisher(
            UpdateStatus,
            '/update_order_status',
            10)

        self.order_queue = Queue()  # 선입선출
        self.current_order_id = None
        self.current_order_detail_id = None
        self.current_menu_name = None
        self.current_table_num = None
        self.is_cooking = False
        self.is_serving = False

        # TCP 서버 설정 (웹 클라이언트용)
        self.web_host = '0.0.0.0'
        self.web_port = 12345
        self.server_socket = None

        # `return` 토픽 구독
        self.return_subscription = self.create_subscription(
            String,
            '/return',
            self.handle_return_message,
            10
        )

        # web 서버 스레드 시작
        threading.Thread(target=self.start_web_server, daemon=True).start()

        self.get_logger().info('Task Manager Node Initialized')

    def handle_return_message(self, msg):
        """Handle messages from the `/return` topic."""
        if self.is_serving == False and msg.data.strip() == "return":
            self.get_logger().info('Received return message. Executing start_serve with table_num=0.')

            # `start_serve` 액션 호출
            self.start_serve(0)

    def start_web_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.web_host, self.web_port))
            self.server_socket.listen(5)
            self.get_logger().info(f'Started TCP server on {self.web_host}:{self.web_port}')

            while True:
                client_socket, client_address = self.server_socket.accept()
                self.get_logger().info(f'Accepted connection from {client_address}')
                threading.Thread(target=self.handle_web, args=(client_socket,), daemon=True).start()

        except Exception as e:
            self.get_logger().error(f'Error starting TCP server: {e}')
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_web(self, client_socket):
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                self.get_logger().info(f'Received data from client: {data}')  # web에서 order_id 넘겨줘야 됨

                order_id = int(data.strip())

                self.call_receive_order_service(order_id)

                client_socket.sendall(b'Order received and processing started')
        except Exception as e:
            self.get_logger().error(f'Error handling client: {e}')
        finally:
            client_socket.close()

    def call_receive_order_service(self, order_id):
        if not self.receive_order_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('ReceiveOrder service not available!')
            return

        if self.current_order_id != order_id:
            self.update_status(order_id, 'Processing', 'order')

            if self.current_order_id is not None:
                self.update_status(self.current_order_id, 'Completed', 'order')

        self.current_order_id = order_id

        request = ReceiveOrder.Request()
        request.id = order_id

        future = self.receive_order_client.call_async(request)
        future.add_done_callback(lambda future: self.receive_order_response(future))

    def receive_order_response(self, future):
        try:
            response = future.result()
            details = response.details

            self.get_logger().info(f'Received order: {details}')

            for detail in details:
                self.order_queue.put((detail.order_detail_id, detail.menu_name, detail.table_num))

            if not self.is_cooking:
                self.process_queue()

        except Exception as e:
            self.get_logger().error(f'Failed to receive order response: {e}')

    def process_queue(self):
        if self.order_queue.empty():
            return

        self.is_cooking = True

        order_detail_id, menu_name, table_num = self.order_queue.get()

        self.current_order_detail_id = order_detail_id
        self.current_menu_name = menu_name
        self.current_table_num = int(table_num)

        self.get_logger().info(f'Starting to cook: {menu_name} for Table: {table_num}')

        self.call_start_cook_action()

    def call_start_cook_action(self):
        if not self.start_cook_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('StartCook action server not available!')
            return

        goal_msg = Cook.Goal()
        goal_msg.menu_name = self.current_menu_name

        self.get_logger().info(f'Sending cook request for {self.current_menu_name}')

        send_goal_future = self.start_cook_client.send_goal_async(goal_msg, feedback_callback=self.cook_feedback_callback)
        send_goal_future.add_done_callback(lambda future: self.cook_result_callback(future))

    def cook_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        cook_status = feedback.cook_status
        self.get_logger().info(f'Received cook feedback: {cook_status}')

        self.update_status(self.current_order_detail_id, cook_status, 'cook')

    def cook_result_callback(self, future):
        try:
            goal_handle = future.result()
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(lambda future: self.finish_cooking(future))
        except Exception as e:
            self.get_logger().error(f'Error handling cook result: {e}')

    def finish_cooking(self, future):
        try:
            result = future.result().result
            cook_result = result.cook_result

            self.get_logger().info(f'Cooking completed: {cook_result}')

            self.start_serve(self.current_table_num)

            self.is_cooking = False
            self.process_queue()

        except Exception as e:
            self.get_logger().error(f'Error finishing cooking: {e}')

    def start_serve(self, table_num):
        if not self.start_serve_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('start serve action server not available!')
            return

        goal_msg = Serve.Goal()
        goal_msg.table_num = table_num  # 요청 값으로 테이블 번호 설정

        self.update_status(self.current_order_detail_id, "Delivering", 'cook')
        self.get_logger().info(f'Sending AGV to Table {table_num}')
        
        self.is_serving = True

        send_goal_future = self.start_serve_client.send_goal_async(goal_msg, feedback_callback=self.move_feedback_callback)
        send_goal_future.add_done_callback(lambda future: self.move_result_callback(future))

    def move_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'AGV X: {feedback.x}, Y: {feedback.y}, THETA: {feedback.theta}')

    def move_result_callback(self, future):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error('StartServe goal rejected')
                return

            self.get_logger().info('StartServe goal accepted')

            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(lambda future: self.handle_move_result(future))
        except Exception as e:
            self.get_logger().error(f'Error sending StartServe goal: {e}')

    def handle_move_result(self, future):
        try:
            result = future.result().result
            move_result = result.move_result  # 결과 값
            self.get_logger().info(f'AGV arrived at Table: {self.current_table_num}, Move Result: {move_result}')

            # 상태 업데이트: 음식 배달 완료
            self.update_status(self.current_order_detail_id, "Completed", 'cook')
            self.is_serving = False

        except Exception as e:
            self.get_logger().error(f'Error handling move result: {e}')

    def update_status(self, id, status, cook_or_order):
        status_msg = UpdateStatus()
        status_msg.id = id
        status_msg.status = status

        if cook_or_order == 'cook':
            self.cook_status_publisher.publish(status_msg)
            self.get_logger().info(f'Published cook status update: {id}, {status}')
        else:
            self.order_status_publisher.publish(status_msg)
            self.get_logger().info(f'Published order status update: {id}, {status}')


def main(args=None):
    rclpy.init(args=args)
    node = TaskManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Task Manager Node')
    finally:
        if node.server_socket:
            node.server_socket.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

