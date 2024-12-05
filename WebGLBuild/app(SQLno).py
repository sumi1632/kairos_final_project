from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = '.'

# 메모리에 데이터 저장을 위한 변수들
orders = {}
tables = {}  # 테이블별 주문 관리

# 메뉴 데이터
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

# 템플릿 데이터 생성 함수
def create_template_data(table_id=None):
    return {
        'table_id': table_id,
        'menu_data': MENU_DATA,
        'menu_image_map': MENU_IMAGE_MAP,
        'initial_content': generate_initial_content(table_id)
    }

# 초기 콘텐츠 생성 함수
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
        print(f"\n=== 주문 시작 ===")
        print(f"테이블 ID: {data.get('tableId')}")
        print(f"받은 주문 데이터: {data}")
        
        is_additional = data.get('isAdditional', False)
        table_id = data.get('tableId')
        
        # 테이블 초기화
        if table_id not in tables:
            tables[table_id] = {
                'orders': [],
                'current_order_id': 1,  # 각 테이블별로 주문 ID 관리
                'last_order_time': None
            }
            print(f"새로운 테이블 {table_id} 생성됨")
        
        # 주문 ID 생성
        if not is_additional:
            order_id = f"{table_id}-{tables[table_id]['current_order_id']}"  # 테이블별 고유 주문 ID
            tables[table_id]['current_order_id'] += 1
            print(f"새로운 주문 ID 생성: {order_id}")
        else:
            # 추가 주문의 경우 기존 주문 ID 사용
            order_id = data.get('orderId') or f"{table_id}-{tables[table_id]['current_order_id']}"
            print(f"추가 주문 ID: {order_id}")
        
        # 주문 생성 시간
        order_time = get_korea_time()
        tables[table_id]['last_order_time'] = order_time
        
        if order_id not in orders:
            orders[order_id] = {
                'items': [],
                'status': 'Waiting',
                'total_price': 0,
                'table_id': table_id,
                'created_at': order_time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_additional': is_additional
            }
            print(f"새로운 주문 생성됨: {order_id}")

        # 각 아이템에 대해 개별 시간 생성
        for item in data['items']:
            menu = next((m for m in MENU_DATA if m['menu_id'] == item['menuId']), None)
            if menu:
                item_time = get_korea_time()
                new_item = {
                    'menu_id': item['menuId'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'cook_status': 'Waiting',
                    'menu_name': menu['name'],
                    'is_additional': is_additional,
                    'created_at': item_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                orders[order_id]['items'].append(new_item)
                orders[order_id]['total_price'] += item['price'] * item['quantity']
                print(f"메뉴 추가됨: {menu['name']}")

        # 테이블에 주문 추가
        if order_id not in tables[table_id]['orders']:
            tables[table_id]['orders'].append(order_id)
            print(f"테이블 {table_id}에 주문 {order_id} 추가됨")

        print(f"현재 테이블 상태: {tables}")
        print(f"현재 주문 상태: {orders[order_id]}")
        print("=== 주문 완료 ===\n")

        return jsonify({
            'success': True,
            'orderId': order_id,
            'tableId': table_id,
            'message': '주문이 성공적으로 처리되었습니다.'
        })

    except Exception as e:
        print(f"주문 처리 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/table/<int:table_id>/orders', methods=['GET'])
def get_table_orders(table_id):
    try:
        print(f"\n=== 테이블 {table_id} 주문 조회 시작 ===")
        print(f"전체 테이블 상태: {tables}")
        print(f"전체 주문 상태: {orders}")
        
        active_orders = []
        table_orders = tables.get(table_id, {}).get('orders', [])
        print(f"테이블 {table_id}의 주문 목록: {table_orders}")
        
        for order_id in table_orders:
            if order_id in orders:
                order = orders[order_id]
                if order['table_id'] == table_id:
                    formatted_order = {
                        'order_id': order_id,
                        'total_price': order['total_price'],
                        'order_status': order['status'],
                        'created_at': order.get('created_at'),
                        'is_additional': order.get('is_additional', False),
                        'items': []
                    }
                    
                    for item in order['items']:
                        formatted_item = {
                            'menu_name': item.get('menu_name'),
                            'quantity': item['quantity'],
                            'cook_status': item.get('cook_status', 'Waiting'),
                            'price': item['price'],
                            'is_additional': item.get('is_additional', False)
                        }
                        formatted_order['items'].append(formatted_item)
                    
                    active_orders.append(formatted_order)
                    print(f"주문 {order_id} 추가됨: {formatted_order}")
                else:
                    print(f"주문 {order_id}는 테이블 {table_id}의 주문이 아님")
            else:
                print(f"주문 {order_id}를 찾을 수 없음")
        
        print(f"응답할 주문 목록: {active_orders}")
        print("=== 테이블 주문 조회 완료 ===\n")
        return jsonify(active_orders)
        
    except Exception as e:
        print(f"주문 상태 조회 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/order/<order_id>/menu/<string:menu_name>/status', methods=['PUT'])
def update_menu_status(order_id, menu_name):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
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
        
        # orders 딕셔너리에서 해당 주문 찾기
        if order_id in orders:
            updated = False
            for item in orders[order_id]['items']:
                if item.get('menu_name') == korean_menu_name:
                    item['cook_status'] = new_status
                    updated = True
                    print(f"메뉴 상태 업데이트: {korean_menu_name} -> {new_status}")
            
            if not updated:
                return jsonify({
                    'success': False,
                    'message': f'메뉴를 찾을 수 없습니다: {korean_menu_name}'
                }), 404
            
            # 모든 메뉴가 완료되었는지 확인
            if new_status == 'Completed':
                all_completed = all(item['cook_status'] == 'Completed' 
                                  for item in orders[order_id]['items'])
                if all_completed:
                    orders[order_id]['status'] = 'Completed'
            
            return jsonify({
                'success': True,
                'message': f'{korean_menu_name}의 상태가 {new_status}로 업데이트되었습니다.',
                'current_status': new_status
            })
        else:
            return jsonify({
                'success': False,
                'message': f'주문을 찾을 수 없습니다: {order_id}'
            }), 404
            
    except Exception as e:
        print("메뉴 상태 업데이트 중 오류 발생:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    template_data = create_template_data()
    return render_template('index(SQLno).html', **template_data)

@app.route('/table/<int:table_id>')
def table_view(table_id):
    if table_id not in [1, 2]:
        return "잘못된 테이블 번호입니다.", 404
    template_data = create_template_data(table_id)
    return render_template('index(SQLno).html', **template_data)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)