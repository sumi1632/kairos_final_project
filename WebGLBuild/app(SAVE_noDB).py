from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime, timezone, timedelta

app = Flask(__name__, static_folder='.')
app.template_folder = '.'

# 메모리에 데이터 저장을 위한 변수들
orders = {}
current_order_id = 1
tables = {}  # 테이블별 주문 관리
current_table_id = 1

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
        'Plating': '추가레이팅중',
        'Delivering': '서빙중',
        'Completed': '완료'
    }
    return status_map.get(status, status)

def get_korea_time():
    # 현재 시간을 UTC로 가져오기
    utc_now = datetime.utcnow()
    # 한국 시간대 설정 (UTC+9)
    korea_timezone = timezone(timedelta(hours=9))
    # UTC 시간을 한국 시간으로 변환
    korea_time = utc_now.replace(tzinfo=timezone.utc).astimezone(korea_timezone)
    return korea_time

@app.route('/api/menus', methods=['GET'])
def get_menus():
    menus = MENU_DATA.copy()
    for menu in menus:
        menu['image_url'] = MENU_IMAGE_MAP.get(menu['name'], 'default.png')
    return jsonify(menus)

@app.route('/api/order', methods=['POST'])
def create_order():
    global current_order_id, current_table_id
    try:
        data = request.get_json()
        print("받은 주문 데이터:", data)
        
        is_additional = data.get('isAdditional', False)
        table_id = data.get('tableId')
        
        if not is_additional:
            table_id = current_table_id
            current_table_id += 1
        
        order_id = data.get('orderId') or current_order_id
        
        # 주문 생성 시간
        order_time = get_korea_time()
        
        if order_id not in orders:
            orders[order_id] = {
                'items': [],
                'status': 'Waiting',
                'total_price': 0,
                'table_id': table_id,
                'created_at': order_time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_additional': is_additional
            }
            current_order_id += 1

        # 각 아이템에 대해 개별 시간 생성
        for item in data['items']:
            menu = next((m for m in MENU_DATA if m['menu_id'] == item['menuId']), None)
            if menu:
                # 각 아이템마다 새로운 시간 생성
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
                
                # 디버깅을 위한 시간 출력
                print(f"아이템 '{menu['name']}' 생성 시간: {new_item['created_at']}")

        # 테이블에 주문 추가
        if table_id not in tables:
            tables[table_id] = []
        if order_id not in tables[table_id]:
            tables[table_id].append(order_id)

        print("현재 주문 상태:", orders[order_id])

        return jsonify({
            'success': True,
            'orderId': order_id,
            'tableId': table_id,
            'message': '주문이 성공적으로 처리되었습니다.'
        })

    except Exception as e:
        print("주문 처리 중 오류 발생:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/table/<int:table_id>/orders', methods=['GET'])
def get_table_orders(table_id):
    try:
        active_orders = []
        table_orders = tables.get(table_id, [])
        
        for order_id in table_orders:
            if order_id in orders:
                order = orders[order_id]
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
        
        print("Sending orders:", active_orders)
        return jsonify(active_orders)
        
    except Exception as e:
        print("주문 상태 조회 중 오류 발생:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/order/<int:order_id>/menu/<string:menu_name>/status', methods=['PUT'])
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
        
        if order_id in orders:
            for item in orders[order_id]['items']:
                menu = next((m for m in MENU_DATA if m['menu_id'] == item['menu_id']), None)
                if menu and menu['name'] == korean_menu_name:
                    item['cook_status'] = new_status
            
            # 모든 메뉴가 완료되었을 때만 주문 상태 업데이트
            if new_status == 'Completed':
                all_completed = all(item['cook_status'] == 'Completed' 
                                  for item in orders[order_id]['items'])
                if all_completed:
                    orders[order_id]['status'] = 'Completed'
        
        return jsonify({
            'success': True,
            'message': f'{korean_menu_name}의 상태가 {new_status}로 업데이트되었습니다.'
        })
        
    except Exception as e:
        print("메뉴 상태 업데이트 중 오류 발생:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index(SAVE_noDB).html')

@app.route('/Build/<path:filename>')
def serve_build_files(filename):
    return send_from_directory('Build', filename)

@app.route('/TemplateData/<path:filename>')
def serve_template_data(filename):
    return send_from_directory('TemplateData', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

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
