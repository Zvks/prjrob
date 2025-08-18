import MT5Exchange as MT5Exchange, order as order
from flask import Flask, jsonify, request
import os, json

# Создание экземпляра Flask
app = Flask(__name__)

# Инициализация MT5Exchange
mt5_exchange = MT5Exchange.MT5Exchange()
if not(mt5_exchange.check_config_exists()):
    mt5_exchange.create_config()
mt5_exchange.read_config_ini_to_json()
login = mt5_exchange.config_dict['authorization']['login']
password = mt5_exchange.config_dict['authorization']['password']
server = mt5_exchange.config_dict['authorization']['server']
print(login, password, server)
order = order.Ord(login, password, server)

@app.route('/data/json', methods=['GET'])
def get_data_json():
    try:
        data = mt5_exchange.config_dict
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Ошибка чтения JSON: {str(e)}"}), 500

@app.route('/create_order', methods=['POST'])
def create_order():
    """
    Создание ордера через HTTP-запрос
    Параметры (JSON):
    - order_type: "buy", "sell", "buy_limit", "sell_limit", "buy_stop", "sell_stop"
    - symbol: торговый символ (например, "EURUSD")
    - lot: объем в лотах
    - price: цена для отложенных ордеров (опционально)
    - sl_ratio: соотношение для стоп-лосса (опционально)
    - tp_ratio: соотношение для тейк-профита (опционально)
    """
    try:
        data = request.get_json()
        
        required_fields = ['order_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
        
        result = order.createOrder(
            order_type=data['order_type'],
            symbol=data.get('symbol', 'EURUSD'),
            lot=float(data.get('lot', 0.1)),
            price=float(data['price']) if 'price' in data else None,
            sl_ratio=float(data['sl_ratio']) if 'sl_ratio' in data else None,
            tp_ratio=float(data['tp_ratio']) if 'tp_ratio' in data else None
        )
        
        return jsonify({'status': 'success', 'result': result})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/update_order', methods=['POST'])
def update_order():
    """
    Обновление ордера/позиции через HTTP-запрос
    Параметры (JSON):
    - ticket: номер тикета (опционально, если не указан - массовое обновление)
    - order_type: "position" или "pending"
    - filter_type: "all", "buy", "sell", "buy_limit" и т.д. (опционально)
    - filter_symbol: "all" или конкретный символ (опционально)
    - new_price: новая цена (только для отложенных ордеров, опционально)
    - down_max: максимальный процент для SL (опционально)
    - up_max: максимальный процент для TP (опционально)
    """
    try:
        data = request.get_json()
        
        if 'order_type' not in data:
            return jsonify({'status': 'error', 'message': 'Missing required field: order_type'}), 400
        
        result = order.updateOrder(
            ticket=int(data['ticket']) if 'ticket' in data else None,
            order_type=data['order_type'],
            filter_type=data.get('filter_type', 'all'),
            filter_symbol=data.get('filter_symbol', 'all'),
            new_price=float(data['new_price']) if 'new_price' in data else None,
            down_max=float(data.get('down_max', 2)),
            up_max=float(data.get('up_max', 30))
        )
        
        return jsonify({'status': 'success', 'result': result})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/close_order', methods=['POST'])
def close_order():
    """
    Закрытие ордера/позиции через HTTP-запрос
    Параметры (JSON):
    - ticket: номер тикета (опционально, если не указан - массовое закрытие)
    - order_type: "position" или "pending"
    - filter_type: "all", "buy", "sell" и т.д. (опционально)
    - filter_symbol: "all" или конкретный символ (опционально)
    """
    try:
        data = request.get_json()
        
        if 'order_type' not in data:
            return jsonify({'status': 'error', 'message': 'Missing required field: order_type'}), 400
        
        result = order.closeOrder(
            ticket=int(data['ticket']) if 'ticket' in data else None,
            order_type=data['order_type'],
            filter_type=data.get('filter_type', 'all'),
            filter_symbol=data.get('filter_symbol', 'all')
        )
        
        return jsonify({'status': 'success', 'result': result})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/read_order', methods=['GET'])
def read_order():
    """
    Получение информации об ордерах/позициях через HTTP-запрос
    Параметры (query parameters):
    - order_type: "position", "pending" или "all" (по умолчанию "all")
    - filter_type: "all", "buy", "sell" и т.д. (опционально)
    - filter_symbol: "all" или конкретный символ (опционально)
    """
    try:
        order_type = request.args.get('order_type', 'all')
        filter_type = request.args.get('filter_type', 'all')
        filter_symbol = request.args.get('filter_symbol', 'all')
        
        result = order.readOrder(
            order_type=order_type,
            filter_type=filter_type,
            filter_symbol=filter_symbol
        )
        
        # Преобразуем объекты MT5 в словари для JSON
        if result is not None:
            result = [obj._asdict() for obj in result]
        
        return jsonify({'status': 'success', 'result': result})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    return 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)