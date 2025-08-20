from flask import Flask, jsonify, request

app = Flask(__name__)

# Простой маршрут для GET запроса
@app.route('/')
def home():
    return jsonify({"message": "Привет от сервера Flask!"})

# Маршрут для получения данных
@app.route('/api/data')
def get_data():
    data = {
        "name": "Сервер Flask",
        "version": "1.0",
        "status": "работает"
    }
    return jsonify(data)

# Маршрут для POST запроса
@app.route('/api/echo', methods=['POST'])
def echo():
    content = request.json
    return jsonify({
        "received": content,
        "message": "Данные успешно получены сервером"
    })

# Маршрут с параметрами
@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user_data = {
        "id": user_id,
        "name": f"Пользователь {user_id}",
        "email": f"user{user_id}@example.com"
    }
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)