import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_custom_msgs.action import Cook
from my_custom_msgs.srv import ReceiveOrder
from my_custom_msgs.srv import UpdateStatus
from std_msgs.msg import String
from queue import Queue
import socket
import threading


class TaskManager(Node):
    def __init__(self):
        super().__init__('task_manager_node')

        self.start_cook_client = ActionClient(self, Cook, 'start_cook')

        self.receive_order_client = self.create_client(ReceiveOrder, 'receive_order')

        self.location_publisher = self.create_publisher(
            String,
            '/move_to_location',
            10)
            
        self.cook_status_publisher = self.create_publisher(
            UpdateStatus,
            '/update_cook_status',
            10)
        
        self.order_status_publisher = self.create_publisher(
            UpdateStatus,
            '/update_order_status',
            10)

        self.order_queue = Queue() # 선입선출
	self.current_order_id = None
	self.current_order_detail_id = None
	self.current_menu_name = None
	self.current_table_num = None
	self.is_cooking = False
	
        # TCP 서버 설정 (웹 클라이언트용)
        self.web_host = '0.0.0.0'
        self.web_port = 12345
        self.server_socket = None

        # ESP32와의 통신 설정
        self.esp_host = '0.0.0.0'
        self.esp_port = 12346
        self.esp_socket = None

        # web 서버 스레드 시작
        threading.Thread(target=self.start_web_server, daemon=True).start()

        # ESP32 통신 스레드 시작
        threading.Thread(target=self.start_esp_server, daemon=True).start()

        self.get_logger().info('Task Manager Node Initialized')

    def start_web_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.tcp_host, self.tcp_port))
            self.server_socket.listen(5)
            self.get_logger().info(f'Started TCP server on {self.tcp_host}:{self.tcp_port}')

            while True:
                client_socket, client_address = self.server_socket.accept()
                self.get_logger().info(f'Accepted connection from {client_address}')
                threading.Thread(target=self.handle_web, args=(client_socket,), daemon=True).start()

        except Exception as e:
            self.get_logger().error(f'Error starting TCP server: {e}')
        finally:
            if self.server_socket:
                self.server_socket.close()

    def start_esp_server(self):
        try:
            self.esp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.esp_socket.bind((self.esp_host, self.esp_port))
            self.esp_socket.listen(5)
            self.get_logger().info(f'Started ESP32 server on {self.esp_host}:{self.esp_port}')

            while True:
                client_socket, client_address = self.esp_socket.accept()
                self.get_logger().info(f'ESP32 connected from {client_address}')
                threading.Thread(target=self.handle_esp, args=(client_socket,), daemon=True).start()

        except Exception as e:
            self.get_logger().error(f'Error starting ESP32 server: {e}')
        finally:
            if self.esp_socket:
                self.esp_socket.close()

    def handle_web(self, client_socket):
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                self.get_logger().info(f'Received data from client: {data}') # web에서 order_id 넘겨줘야 됨

                order_id = int(data.strip())
                
                self.call_receive_order_service(order_id)

                client_socket.sendall(b'Order received and processing started')
        except Exception as e:
            self.get_logger().error(f'Error handling client: {e}')
        finally:
            client_socket.close()

    def handle_esp(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    self.get_logger().info(f'Received data from ESP32: {data}')

                    if data.startswith('MOVE'):
                        table_num = data.split(' ')[1]  # 예: "MOVE 5"
                        self.move_to_location(int(table_num))

        except Exception as e:
            self.get_logger().error(f'Error handling ESP32: {e}')
        finally:
            client_socket.close()

# 웹에서 order_id 받으면 order_detail(요리 하나씩) 테이블 값들 받아오기
    def call_receive_order_service(self, order_id):
        if not self.receive_order_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('ReceiveOrder service not available!')
            return
        
	# 새로운 요리 시작
        if self.current_order_id != order_id:
            self.update_status(order_id, 'In Progress', 'order')
	    # 이전 요리 종료
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
                self.order_queue.put(detail)
	# 음식 조리 중이 아닐 때
	if self.is_cooking == False:
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
	self.current_table_num = table_num        
        
        self.get_logger().info(f'Starting to cook: {menu_name} for Table: {table_num}')

        self.call_start_cook_action()

# 로봇암 조리 시작!
    def call_start_cook_action(self):
        if not self.start_cook_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('StartCook action server not available!')
            return

        goal_msg = Cook.Goal()
        goal_msg.menu_name = self.current_menu_name

        self.get_logger().info(f'Sending cook request for {menu_name}')

        send_goal_future = self.start_cook_client.send_goal_async(goal_msg, feedback_callback=self.cook_feedback_callback)
        send_goal_future.add_done_callback(lambda future: self.cook_result_callback(future))

# 요리 진행 상황에 따라 cook_status('Waiting', 'Preparing', 'Cooking', 'Plating', 'Delivering', 'Completed') 바꿔줘야 됨
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
            
# 여기에 cook status completed로 바꿔줘야될지 피드백에서 바꾸면 될지 고민
    def finish_cooking(self, future):
        try:
            result = future.result().result
            cook_result = result.cook_result

            self.get_logger().info(f'Cooking completed: {cook_result}')

            self.move_to_location(self.current_table_num)
            
            # 주문이 더 있을 때 새로운 요리 시작
            self.is_cooking = False
            self.process_queue()
            
        except Exception as e:
            self.get_logger().error(f'Error finishing cooking: {e}')

    def move_to_location(self, table_num):
        msg = String()
        msg.data = str(table_num)
        self.location_publisher.publish(msg)
        self.get_logger().info(f'Moving to Table {table_num}')
        
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
        if node.esp_socket:
            node.esp_socket.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
