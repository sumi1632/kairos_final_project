import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from custom_msgs.srv import ReceiveOrder
from custom_msgs.msg import UpdateStatus
from custom_msgs.msg import OrderDetail
import mysql.connector


class DBManagerNode(Node):
    def __init__(self):
        super().__init__('db_manager_node')

        # MySQL 연결 설정
        self.db = mysql.connector.connect(
            host='172.30.1.43',  # MySQL 서버 주소
            user='manager',       # MySQL 사용자
            password='1234',   # MySQL 비밀번호
            database='yori_db' # 데이터베이스 이름
        )
        self.cursor = self.db.cursor(dictionary=True)  # 결과를 딕셔너리 형식으로 반환

        self.receive_order_service = self.create_service(
            ReceiveOrder, 'receive_order', self.handle_receive_order
        )

        self.update_order_status_sub = self.create_subscription(
            UpdateStatus,
            'update_order_status',
            self.update_order_status_callback,
            QoSProfile(depth=10)
        )

        self.update_cook_status_sub = self.create_subscription(
            UpdateStatus,
            'update_cook_status',
            self.update_cook_status_callback,
            QoSProfile(depth=10)
        )

        self.get_logger().info('DB Manager Node has been started.')

    def handle_receive_order(self, request, response):
        order_id = int(request.id)  # 요청 값에서 order_id 가져오기
        self.get_logger().info(f"Received order_id: {order_id}")

        try:
            query = """
		    SELECT 
		        order_detail.order_detail_id AS order_detail_id,
		        menu.name AS menu_name,
		        restaurant_table.table_num AS table_num
		    FROM 
		        order_detail
		    JOIN 
		        menu ON order_detail.menu_id = menu.menu_id
		    JOIN 
		        restaurant_table ON order_detail.table_id = restaurant_table.table_id
		    WHERE 
		        order_detail.order_id = %s
		"""
            self.cursor.execute(query, (order_id,))
            results = self.cursor.fetchall()
            response.details = [
	        self.create_order_detail(
	            result["order_detail_id"],
	            result["menu_name"],
	            result["table_num"]
	        ) for result in results]

            self.get_logger().info(f"Query Results: {response.details}")

        except Exception as e:
            self.get_logger().error(f"Error retrieving order details: {e}")
            response.details = []

        return response
        
    def create_order_detail(self, order_detail_id, menu_name, table_num):
        detail = OrderDetail()
        detail.order_detail_id = order_detail_id
        detail.menu_name = menu_name
        detail.table_num = table_num
        return detail

    def update_order_status_callback(self, msg):
        order_id = msg.id
        new_status = msg.status
        self.get_logger().info(f"Updating order_status for order_id {order_id} to {new_status}")

        try:
            # orders 테이블 업데이트
            query = """
                UPDATE orders
                SET order_status = %s
                WHERE order_id = %s
            """
            self.cursor.execute(query, (new_status, order_id))
            self.db.commit()
            self.get_logger().info(f"Order status updated successfully for order_id {order_id}.")
        except Exception as e:
            self.get_logger().error(f"Error updating order status: {e}")

    def update_cook_status_callback(self, msg):
        order_detail_id = msg.id
        new_status = msg.status
        self.get_logger().info(f"Updating cook_status for order_detail_id {order_detail_id} to {new_status}")

        try:
            query = """
                UPDATE order_detail
                SET cook_status = %s
                WHERE order_detail_id = %s
            """
            self.cursor.execute(query, (new_status, order_detail_id))
            self.db.commit()
            self.get_logger().info(f"Cook status updated successfully for order_detail_id {order_detail_id}.")
        except Exception as e:
            self.get_logger().error(f"Error updating cook status: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = DBManagerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down node...')
    finally:
        node.cursor.close()
        node.db.close()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

