import requests
import time
import json

# Глобальные переменные (объявляем заранее)
RABBITMQ_API = None
USERNAME = None
PASSWORD = None
VHOST = None
EXCHANGE_TYPE = None

def exchange_exists(exchange_name):
    """Проверяет, существует ли exchange."""
    url = f"{RABBITMQ_API}/api/exchanges/{VHOST}/{exchange_name}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    return response.status_code == 200

def create_exchange(exchange_name):
    """Создаёт exchange, если он не существует."""
    if exchange_exists(exchange_name):
        print(f"Exchange '{exchange_name}' уже существует.")
        return True

    url = f"{RABBITMQ_API}/api/exchanges/{VHOST}/{exchange_name}"
    data = {
        "type": EXCHANGE_TYPE,
        "durable": True,
        "auto_delete": False,
        "internal": False,
        "arguments": {}
    }

    response = requests.put(url, data=json.dumps(data), auth=(USERNAME, PASSWORD), headers={"Content-Type": "application/json"})

    if response.status_code in [201, 204]:
        print(f"Exchange '{exchange_name}' успешно создан или обновлён.")
        return True
    else:
        print(f"Ошибка при создании exchange: {response.status_code} - {response.text}")
        return False
        
def create_queue(exchange_name, queue_name):
    """Создаёт очередь."""
    url = f"{RABBITMQ_API}/api/queues/{VHOST}/{queue_name}"
    data = {
        "durable": True,
        "auto_delete": False,
        "exclusive": False,
        "arguments": {}
    }
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, data=json.dumps(data), headers=headers, auth=(USERNAME, PASSWORD))
    if response.status_code in (201, 204):
        print(f"Очередь '{queue_name}' создана или уже существует.")
        bind_queue_to_exchange(exchange_name, queue_name)
        return True
    else:
        print(f"Ошибка при создании очереди '{queue_name}': {response.status_code}, {response.text}")
        return False

def bind_queue_to_exchange(exchange_name, queue_name):
    """Привязывает очередь к exchange с routing_key = имени очереди."""
    url = f"{RABBITMQ_API}/api/bindings/{VHOST}/e/{exchange_name}/q/{queue_name}"
    data = {
        "routing_key": queue_name  # можно использовать другое, если нужно
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers, auth=(USERNAME, PASSWORD))
    if response.status_code == 201:
        print(f"Очередь '{queue_name}' привязана к exchange с routing_key='{queue_name}'.")
        return True
    else:
        print(f"Ошибка привязки очереди '{queue_name}': {response.status_code}, {response.text}")
        return False
    
def get_config(url):
    """Получает конфигурацию из URL и устанавливает глобальные переменные."""
    # Выполняем GET-запрос
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим JSON
        data = response.json()
        
        # Устанавливаем глобальные переменные
        global RABBITMQ_API, USERNAME, PASSWORD, VHOST, EXCHANGE_TYPE
        RABBITMQ_API = data["rabbitMQ"]["rabbitmq_api"]
        USERNAME = data["rabbitMQ"]["username"]
        PASSWORD = data["rabbitMQ"]["password"]
        VHOST = data["rabbitMQ"]["vhost"]
        EXCHANGE_TYPE = data["rabbitMQ"]["exchange_type"]

        return data
    else:
        print(f"Ошибка: {response.status_code}")
        return response.status_code

url_config = "http://192.168.1.160:5050/data/json"
while (True):
    data = get_config(url_config)
    instruments = str(data["instruments"]["instruments"]).split(",")
    print(instruments)
    for i in instruments:
        create_exchange(i)
        create_queue(i, i + "_bars")
        create_queue(i, i + "_ord")
        print(i)
    time.sleep(300)