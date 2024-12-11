from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime, timezone, timedelta
import mysql.connector
import socket

app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = '.'

# DB 연결 정보 추가
db_config = {
    "host": "172.30.1.43",
    "user": "manager",
    "password": "1234",
    "database": "yori_db"
}

# TCP 클라이언트 설정 추가
TCP_SERVER_HOST = '172.30.1.11'
TCP_SERVER_PORT = 12345

orders = {}
tables = {}  # 테이블별 주문 관리
item_id_counter = 0

MENU_DATA = [
    {"menu_id": 1, "name": "튀김덮밥", "description": "바삭한 튀김과 특제 소스의 조화", "price": 12000},
    {"menu_id": 2, "name": "장어덮밥", "description": "달콤한 장어구이와 특제 양념", "price": 15000},
    {"menu_id": 3, "name": "비빔밥", "description": "신선한 야채와 고소한 참기름", "price": 11000},
    {"menu_id": 4, "name": "국수", "description": "쫄깃한 면발과 시원한 국물", "price": 9000}
]

MENU_IMAGE_MAP = {
    '튀김덮밥': 'tempura.png',
    '장어덮밥': 'eel.png',
    '비빔밥': 'bibimbap.png',
    '국수': 'noodles.png'
}

def send_order_to_tcp_server(order_id):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
        message = str(order_id)
        client_socket.send(message.encode())
        print(f"주문 ID {order_id}를 TCP 서버로 전송 완료")
    except Exception as e:
        print(f"TCP 서버 전송 중 오류 발생: {str(e)}")
    finally:
        client_socket.close()

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

def get_korea_time():
    utc_now = datetime.utcnow()
    korea_timezone = timezone(timedelta(hours=9))
    korea_time = utc_now.replace(tzinfo=timezone.utc).astimezone(korea_timezone)
    return korea_time

def create_template_data(table_id=None):
    return {
        'table_id': table_id,
        'menu_data': MENU_DATA,
        'menu_image_map': MENU_IMAGE_MAP,
        'initial_content': generate_initial_content(table_id)
    }

def generate_initial_content(table_id):
    if table_id is None:
        return """
            <div class="header">
                <h1>요리조리 식당</h1>
            </div>
            <div style="text-align: center; padding: 2rem;">
                <h2>테이블을 선택해주세요:</h2>
                <div style="margin-top: 2rem;">
                    <a href="/table/1" class="table-button">테이블 1</a>
                    <a href="/table/2" class="table-button">테이블 2</a>
                </div>
            </div>
        """
    else:
        return """
            <div class="header">
                <h1>요리조리 식당</h1>
                <h2>테이블 {}</h2>
            </div>
            <div class="menu-section">
                <div class="menu-grid" id="menuGrid"></div>
            </div>
            <div id="cartSection" class="cart-section">
                <div class="cart-items" id="cartItems"></div>
                <div class="cart-total">
                    <span>총액:</span>
                    <span class="total-amount">0원</span>
                </div>
                <button class="checkout-btn" onclick="startPayment()">주문하기</button>
            </div>
            <div id="mainOrderStatusSection" class="order-status-section" style="display: none;">
                <div id="orderList" class="order-list"></div>
            </div>
        """.format(table_id)

@app.route('/api/menus', methods=['GET'])
def get_menus():
    menus = MENU_DATA.copy()
    for menu in menus:
        menu['image_url'] = MENU_IMAGE_MAP.get(menu['name'], 'default.png')
    return jsonify(menus)

@app.route('/api/order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        print("받은 주문 데이터:", data)
        
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        
        cursor.execute("START TRANSACTION")
        
        table_id = data.get('tableId')
        
        cursor.execute("""
            INSERT INTO orders (table_id, total_price, order_status)
            VALUES (%s, 0, 'Waiting')
        """, (table_id,))
        
        order_id = cursor.lastrowid
        
        total_price = 0
        for item in data['items']:
            cursor.execute("""
                INSERT INTO order_detail (order_id, menu_id, quantity, table_id)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item['menuId'], item['quantity'], table_id))
            total_price += item['price'] * item['quantity']
        
        cursor.execute("""
            UPDATE orders 
            SET total_price = %s
            WHERE order_id = %s
        """, (total_price, order_id))
        
        db.commit()
        
        send_order_to_tcp_server(order_id)
        
        return jsonify({
            'success': True,
            'orderId': order_id,
            'tableId': table_id,
            'message': '주문이 성공적으로 처리되었습니다.'
        })
        
    except Exception as e:
        if 'db' in locals(): 
            db.rollback()
        print(f"주문 처리 중 오류 발생: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '주문 처리 중 오류가 발생했습니다.'
        }), 500
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

@app.route('/api/table/<int:table_id>/orders', methods=['GET'])
def get_table_orders(table_id):
    try:
        print(f"\n=== 테이블 {table_id} 주문 조회 시작 ===")
        
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT o.order_id, o.table_id, o.total_price, o.order_status, o.created_at,
                   od.menu_id, od.quantity, od.cook_status,
                   m.name as menu_name, m.price
            FROM orders o
            JOIN order_detail od ON o.order_id = od.order_id
            JOIN menu m ON od.menu_id = m.menu_id
            WHERE o.table_id = %s
            AND o.order_status != 'Completed'
            AND o.order_id = (
                SELECT MAX(order_id) 
                FROM orders 
                WHERE table_id = %s AND order_status != 'Completed'
            )
            ORDER BY o.created_at DESC
        """, (table_id, table_id))
        
        orders_data = cursor.fetchall()
        
        formatted_orders = {}
        for row in orders_data:
            order_id = row['order_id']
            
            if order_id not in formatted_orders:
                formatted_orders[order_id] = {
                    'order_id': order_id,
                    'table_id': row['table_id'],
                    'total_price': row['total_price'],
                    'order_status': row['order_status'],
                    'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S') if row['created_at'] else None,
                    'items': []
                }
            
            formatted_orders[order_id]['items'].append({
                'menu_name': row['menu_name'],
                'quantity': row['quantity'],
                'cook_status': row['cook_status'] or 'Waiting',
                'price': row['price'],
                'menu_id': row['menu_id']
            })
        
        active_orders = list(formatted_orders.values())
        print(f"응답할 주문 목록: {active_orders}")
        print("=== 테이블 주문 조회 완료 ===\n")
        
        return jsonify(active_orders)
        
    except Exception as e:
        print(f"주문 상태 조회 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

@app.route('/api/table/<int:table_id>/past_orders', methods=['GET'])
def get_past_orders(table_id):
    try:
        print(f"\n=== 테이블 {table_id} 지난 주문 조회 시작 ===")
        
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT o.order_id, o.table_id, o.total_price, o.order_status, o.created_at,
                   od.menu_id, od.quantity, od.cook_status,
                   m.name as menu_name, m.price
            FROM orders o
            JOIN order_detail od ON o.order_id = od.order_id
            JOIN menu m ON od.menu_id = m.menu_id
            WHERE o.table_id = %s
            AND o.order_status = 'Completed'
            ORDER BY o.created_at DESC
            LIMIT 10
        """, (table_id,))
        
        past_orders_data = cursor.fetchall()
        
        formatted_orders = {}
        for row in past_orders_data:
            order_id = row['order_id']
            
            if order_id not in formatted_orders:
                formatted_orders[order_id] = {
                    'order_id': order_id,
                    'table_id': row['table_id'],
                    'total_price': row['total_price'],
                    'order_status': row['order_status'],
                    'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S') if row['created_at'] else None,
                    'items': []
                }
            
            formatted_orders[order_id]['items'].append({
                'menu_name': row['menu_name'],
                'quantity': row['quantity'],
                'cook_status': row['cook_status'] or 'Completed',
                'price': row['price'],
                'menu_id': row['menu_id']
            })
        
        past_orders = list(formatted_orders.values())
        
        print(f"응답할 지난 주문 목록: {past_orders}")
        print("=== 지난 주문 조회 완료 ===\n")
        
        return jsonify(past_orders)
        
    except Exception as e:
        print(f"지난 주문 상태 조회 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

@app.route('/api/order/<order_id>/menu/<string:menu_name>/status', methods=['GET'])
def update_menu_status(order_id, menu_name):
    try:
        data = request.get_json()
        
        print(f"\n=== 상태 조회 시작 ===")
        print(f"주문 ID: {order_id}")
        print(f"메뉴: {menu_name}")
        
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        
        # 해당 주문 ID와 메뉴 이름에 해당하는 cook_status 조회
        cursor.execute("""
            SELECT od.cook_status 
            FROM order_detail od
            JOIN menu m ON od.menu_id = m.menu_id
            WHERE od.order_id = %s AND m.name = %s
        """, (order_id, menu_name))
        
        result = cursor.fetchone()
        
        if not result:
            return jsonify({
                'success': False,
                'message': f"주문 {order_id}에 해당하는 {menu_name} 메뉴 정보를 찾을 수 없습니다."
            }), 404
        
        current_status = result['cook_status'] if result['cook_status'] else 'Waiting'
        current_time = get_korea_time().strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'message': f'{menu_name}의 현재 상태는 {current_status} 입니다.',
            'current_status': current_status,
            'updated_at': current_time
        })
        
    except Exception as e:
        if 'db' in locals(): 
            db.rollback()
        print(f"상태 조회 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()


@app.route('/')
def index():
    template_data = create_template_data()
    return render_template('index.html', **template_data)

@app.route('/table/<int:table_id>')
def table_view(table_id):
    if table_id not in [1, 2]:
        return "잘못된 테이블 번호입니다.", 404
    template_data = create_template_data(table_id)
    return render_template('index.html', **template_data)

@app.route('/Build/<path:filename>')
def serve_build_files(filename):
    return send_from_directory('static/Build', filename, max_age=0)

@app.route('/TemplateData/<path:filename>')
def serve_template_data(filename):
    return send_from_directory('static/TemplateData', filename, max_age=0)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename, max_age=0)

@app.route('/api/orders/all', methods=['GET'])
def get_all_orders():
    try:
        all_orders = []
        for order_id, order in orders.items():
            formatted_order = {
                'order_id': order_id,
                'total_price': order['total_price'],
                'order_status': order['status'],
                'created_at': order.get('created_at'),
                'is_additional': order.get('is_additional', False),
                'items': []
            }
            
            for item in order['items']:
                formatted_order['items'].append({
                    'menu_name': item.get('menu_name'),
                    'quantity': item['quantity'],
                    'cook_status': item.get('cook_status', 'Waiting'),
                    'price': item['price']
                })
            
            all_orders.append(formatted_order)
        
        return jsonify(all_orders)
        
    except Exception as e:
        print("전체 주문 조회 중 오류 발생:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin_view():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        
        total_stats = {
            'total_revenue': 0,
            'menu_stats': {
                '튀김덮밥': {'quantity': 0, 'revenue': 0},
                '장어덮밥': {'quantity': 0, 'revenue': 0},
                '비빔밥': {'quantity': 0, 'revenue': 0},
                '국수': {'quantity': 0, 'revenue': 0}
            }
        }
        
        cursor.execute("""
            SELECT m.name, 
                   COALESCE(SUM(od.quantity), 0) as total_quantity,
                   COALESCE(SUM(od.quantity * m.price), 0) as total_revenue
            FROM menu m
            LEFT JOIN order_detail od ON m.menu_id = od.menu_id
            GROUP BY m.name
        """)
        
        menu_stats = cursor.fetchall()
        for stat in menu_stats:
            menu_name = stat['name']
            if menu_name in total_stats['menu_stats']:
                total_stats['menu_stats'][menu_name]['quantity'] = int(stat['total_quantity'])
                total_stats['menu_stats'][menu_name]['revenue'] = int(stat['total_revenue'])
                total_stats['total_revenue'] += int(stat['total_revenue'])
        
        current_cooking = {
            1: {'menu_name': None, 'status': None, 'order_id': None, 'last_updated': None, 'item_id': None},
            2: {'menu_name': None, 'status': None, 'order_id': None, 'last_updated': None, 'item_id': None}
        }
        
        for tbl_id in [1, 2]:
            cursor.execute("""
                SELECT o.order_id, m.name as menu_name, 
                       COALESCE(od.cook_status, 'Waiting') as cook_status, 
                       o.created_at, od.order_detail_id as item_id
                FROM orders o
                JOIN order_detail od ON o.order_id = od.order_id
                JOIN menu m ON od.menu_id = m.menu_id
                WHERE o.table_id = %s 
                AND (od.cook_status IS NULL OR od.cook_status != 'Completed')
                ORDER BY o.created_at DESC, od.order_detail_id DESC
                LIMIT 1
            """, (tbl_id,))
            
            latest_order = cursor.fetchone()
            if latest_order:
                current_cooking[tbl_id] = {
                    'menu_name': latest_order['menu_name'],
                    'status': latest_order['cook_status'],
                    'order_id': latest_order['order_id'],
                    'last_updated': latest_order['created_at'].strftime('%Y-%m-%d %H:%M:%S') if latest_order['created_at'] else None,
                    'item_id': latest_order['item_id']
                }
        
        cursor.execute("SELECT menu_id, name, description, price FROM menu")
        menu_data = cursor.fetchall()
        
        formatted_menu_data = []
        for menu in menu_data:
            formatted_menu_data.append({
                'menu_id': menu['menu_id'],
                'name': menu['name'],
                'description': menu['description'],
                'price': menu['price']
            })
        
        return render_template(
            'admin.html',
            total_stats=total_stats,
            current_cooking=current_cooking,
            menu_data=formatted_menu_data
        )
        
    except Exception as e:
        print(f"관리자 페이지 로드 중 오류 발생: {str(e)}")
        return f"오류가 발생했습니다: {str(e)}", 500
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
