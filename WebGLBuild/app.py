from flask import Flask, render_template, request, jsonify, send_from_directory
import mysql.connector
import os
from datetime import datetime
import socket

app = Flask(__name__, static_folder='.')
app.template_folder = '.'

# 데이터베이스 연결 정보
db_config = {
    "host": "172.30.1.43",
    "user": "manager",
    "password": "1234",
    "database": "yori_db"
}

# app.py에 추가할 매핑 정보
MENU_IMAGE_MAP = {
    '튀김덮밥': 'tempura.png',
    '장어덮밥': 'eel.png',
    '비빔밥': 'bibimbap.png',
    '국수': 'noodles.png'
}

# TCP 클라이언트 설정
TCP_SERVER_HOST = '172.30.1.43'  # 서버 IP 주소
TCP_SERVER_PORT = 12345         # 서버 포트

def send_order_to_tcp_server(order_id):
    try:
        # TCP 소켓 생성
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
        
        # order_id를 문자열로 변환하여 전송
        message = str(order_id)
        client_socket.send(message.encode())
        
        print(f"주문 ID {order_id}를 TCP 서버로 전송 완료")
        
    except Exception as e:
        print(f"TCP 서버 전송 중 오류 발생: {str(e)}")
        
    finally:
        client_socket.close()

# 상태 텍스트 변환 함수 추가
def getStatusText(status):
    status_map = {
        'Waiting': '대기중',
        'Preparing': '재료 준비중',
        'Cooking': '조리중',
        'Plating': '플레이팅중',
        'Delivering': '서빙중',
        'Completed': '완료'
    }
    return status_map.get(status, status)

# 메뉴 조회 API
@app.route('/api/menus', methods=['GET'])
def get_menus():
    db = None
    cursor = None
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT menu_id, name, description, price 
            FROM menu 
            WHERE is_available = TRUE
        """)
        menus = cursor.fetchall()
        
        # 이미지 파일명 추가
        for menu in menus:
            menu['image_url'] = MENU_IMAGE_MAP.get(menu['name'], 'default.png')
        
        return jsonify(menus)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# 주문 처리 API
@app.route('/api/order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        print("받은 주문 데이터:", data)
        
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # 트랜잭션 시작
        cursor.execute("START TRANSACTION")

        # 테이블 ID 가져오기 (테이블 번호 1 사용)
        cursor.execute("SELECT table_id FROM restaurant_table WHERE table_num = 1")
        table_id = cursor.fetchone()[0]

        # 기존 주문인 경우
        if 'orderId' in data and data['orderId']:
            order_id = data['orderId']
            # 기존 주문의 total_price 업데이트
            total_price = sum(item['price'] * item['quantity'] for item in data['items'])
            cursor.execute("""
                UPDATE orders 
                SET total_price = total_price + %s
                WHERE order_id = %s
            """, (total_price, order_id))
        else:
            # 새로운 주문인 경우
            total_price = sum(item['price'] * item['quantity'] for item in data['items'])
            cursor.execute("""
                INSERT INTO orders (table_id, total_price, order_status)
                VALUES (%s, %s, 'Waiting')
            """, (table_id, total_price))
            order_id = cursor.lastrowid

        # order_detail 테이블에 주문 상세 정보 삽입
        for item in data['items']:
            cursor.execute("""
                INSERT INTO order_detail (order_id, menu_id, table_id, cook_status)
                VALUES (%s, %s, %s, 'Waiting')
            """, (order_id, item['menuId'], table_id))

        db.commit()
        print(f"주문 처리 완료 - order_id: {order_id}")
        
        # 주문 완료 후 TCP 서버로 order_id 전송
        send_order_to_tcp_server(order_id)
        
        return jsonify({
            'success': True,
            'orderId': order_id,
            'message': '주문이 성공적으로 처리되었습니다.'
        })

    except Exception as e:
        print("주문 처리 중 오류 발생:", str(e))
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# Flask 라우트 수정
@app.route('/api/table/<int:table_num>/current-orders', methods=['GET'])
def get_current_table_orders(table_num):
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        
        # 현재 진행 중인 주문만 가져오는 쿼리
        cursor.execute("""
            SELECT 
                o.order_id,
                o.total_price,
                o.order_status,
                od.menu_id,
                m.name as menu_name,
                od.cook_status,
                COUNT(od.order_detail_id) as quantity,
                o.created_at
            FROM orders o
            JOIN order_detail od ON o.order_id = od.order_id
            JOIN menu m ON od.menu_id = m.menu_id
            JOIN restaurant_table rt ON o.table_id = rt.table_id
            WHERE rt.table_num = %s
                AND o.order_status != 'Completed'
            GROUP BY 
                o.order_id,
                o.total_price,
                o.order_status,
                od.menu_id,
                m.name,
                od.cook_status,
                o.created_at
            ORDER BY o.created_at DESC
        """, (table_num,))
        
        return format_orders(cursor.fetchall())

@app.route('/api/table/<int:table_num>/past-orders', methods=['GET'])
def get_past_table_orders(table_num):
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        
        # 완료된 주문만 가져오는 쿼리 (최근 10개)
        cursor.execute("""
            SELECT 
                o.order_id,
                o.total_price,
                o.order_status,
                od.menu_id,
                m.name as menu_name,
                od.cook_status,
                COUNT(od.order_detail_id) as quantity,
                o.created_at,
                o.updated_at
            FROM orders o
            JOIN order_detail od ON o.order_id = od.order_id
            JOIN menu m ON od.menu_id = m.menu_id
            JOIN restaurant_table rt ON o.table_id = rt.table_id
            WHERE rt.table_num = %s
                AND o.order_status = 'Completed'
            GROUP BY 
                o.order_id,
                o.total_price,
                o.order_status,
                od.menu_id,
                m.name,
                od.cook_status,
                o.created_at,
                o.updated_at
            ORDER BY o.updated_at DESC
            LIMIT 10
        """, (table_num,))
        
        return format_orders(cursor.fetchall())

def format_orders(orders):
    formatted_orders = {}
    for order in orders:
        order_id = order['order_id']
        if order_id not in formatted_orders:
            formatted_orders[order_id] = {
                'order_id': order_id,
                'total_price': order['total_price'],
                'order_status': order['order_status'],
                'created_at': order['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': order.get('updated_at', '').strftime('%Y-%m-%d %H:%M:%S') if order.get('updated_at') else None,
                'items': []
            }
        
        formatted_orders[order_id]['items'].append({
            'menu_name': order['menu_name'],
            'quantity': order['quantity'],
            'cook_status': order['cook_status']
        })
    
    return jsonify(list(formatted_orders.values()))

# 주문 상태 업데이트 API
@app.route('/api/order/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        # 허용된 상태값 확인
        allowed_statuses = ['Waiting', 'Preparing', 'Cooking', 'Plating', 'Delivering', 'Completed']
        if new_status not in allowed_statuses:
            return jsonify({
                'success': False,
                'message': f'Invalid status. Allowed values are: {", ".join(allowed_statuses)}'
            }), 400
        
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        
        print(f"Updating order {order_id} status to {new_status}")
        
        # 주문 상태 업데이트
        cursor.execute("""
            UPDATE orders 
            SET order_status = %s
            WHERE order_id = %s
        """, (new_status, order_id))
        
        # 주문 상세 상태 업데이트
        cursor.execute("""
            UPDATE order_detail
            SET cook_status = %s
            WHERE order_id = %s
        """, (new_status, order_id))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': f'주문 상태가 {new_status}로 업데이트되었습니다.'
        })
        
    except Exception as e:
        print(f"Error updating order status: {str(e)}")
        db.rollback()
        return jsonify({'error': str(e)}), 500
        
    finally:
        cursor.close()
        db.close()

# 메뉴별 주문 상태 업데이트 API
@app.route('/api/order/<int:order_id>/menu/<string:menu_name>/status', methods=['PUT'])
def update_menu_status(order_id, menu_name):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        # 허용된 상태값 확인
        allowed_statuses = ['Waiting', 'Preparing', 'Cooking', 'Plating', 'Delivering', 'Completed']
        if new_status not in allowed_statuses:
            return jsonify({
                'success': False,
                'message': f'Invalid status. Allowed values are: {", ".join(allowed_statuses)}'
            }), 400
        
        menu_name_map = {
            'tempura_bowl': '튀김덮밥',
            'eel_bowl': '장어덮밥',
            'bibimbap': '비빔밥',
            'noodles': '국수'
        }
        korean_menu_name = menu_name_map.get(menu_name, menu_name)
        
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        
        # 메뉴 상태 업데이트
        cursor.execute("""
            UPDATE order_detail od
            JOIN menu m ON od.menu_id = m.menu_id
            SET od.cook_status = %s,
                od.updated_at = NOW()
            WHERE od.order_id = %s 
            AND m.name = %s
        """, (new_status, order_id, korean_menu_name))
        
        # 모든 메뉴가 완료되었는지 확인
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN cook_status = 'Completed' THEN 1 ELSE 0 END) as completed
            FROM order_detail
            WHERE order_id = %s
        """, (order_id,))
        
        status_count = cursor.fetchone()
        if status_count and status_count[0] == status_count[1]:  # 모든 메뉴가 완료됨
            cursor.execute("""
                UPDATE orders
                SET order_status = 'Completed',
                    updated_at = NOW()
                WHERE order_id = %s
            """, (order_id,))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': f'{korean_menu_name}의 상태가 {new_status}로 업데이트되었습니다.'
        })
        
    except Exception as e:
        print("메뉴 상태 업데이트 중 오류 발생:", str(e))
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500
        
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# 정적 파일 제공을 위한 라우트
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Build/<path:filename>')
def serve_build_files(filename):
    return send_from_directory('Build', filename)

@app.route('/TemplateData/<path:filename>')
def serve_template_data(filename):
    return send_from_directory('TemplateData', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
