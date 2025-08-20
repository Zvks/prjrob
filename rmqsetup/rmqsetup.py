import requests
import json
import pika

# Глобальные переменные
RABBITMQ_HOST = None
RABBITMQ_PORT = 5672
USERNAME = None
PASSWORD = None
VHOST = None
EXCHANGE_TYPE = None

def get_connection():
    """Создает соединение с конкретной нодой RabbitMQ."""
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,  # Указываем конкретную ноду
        port=RABBITMQ_PORT,
        virtual_host=VHOST,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)

def exchange_exists_pika(exchange_name):
    """Проверяет существование exchange через pika."""
    try:
        connection = get_connection()
        channel = connection.channel()
        
        # Пытаемся объявить exchange с passive=True - это проверит существование
        channel.exchange_declare(exchange=exchange_name, passive=True)
        connection.close()
        return True
    except pika.exceptions.ChannelClosedByBroker:
        # Exchange не существует
        connection.close()
        return False
    except Exception as e:
        print(f"Ошибка при проверке exchange: {e}")
        return False

def create_exchange_pika(exchange_name):
    """Создаёт exchange через pika."""
    if exchange_exists_pika(exchange_name):
        print(f"Exchange '{exchange_name}' уже существует.")
        return True

    try:
        connection = get_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=EXCHANGE_TYPE,
            durable=True
        )
        
        connection.close()
        print(f"Exchange '{exchange_name}' успешно создан.")
        return True
    except Exception as e:
        print(f"Ошибка при создании exchange '{exchange_name}': {e}")
        return False

def create_queue_pika(exchange_name, queue_name):
    """Создаёт очередь и привязывает её к exchange через pika."""
    try:
        connection = get_connection()
        channel = connection.channel()
        
        # Создаём очередь
        channel.queue_declare(queue=queue_name, durable=True)
        print(f"Очередь '{queue_name}' создана или уже существует.")
        
        # Привязываем очередь к exchange
        bind_queue_to_exchange_pika(channel, exchange_name, queue_name)
        
        connection.close()
        return True
    except Exception as e:
        print(f"Ошибка при создании очереди '{queue_name}': {e}")
        return False

def bind_queue_to_exchange_pika(channel, exchange_name, queue_name):
    """Привязывает очередь к exchange с routing_key = имени очереди."""
    try:
        channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=queue_name
        )
        print(f"Очередь '{queue_name}' привязана к exchange '{exchange_name}' с routing_key='{queue_name}'.")
    except Exception as e:
        print(f"Ошибка привязки очереди '{queue_name}': {e}")

def get_config(url):
    """Получает конфигурацию из URL и устанавливает глобальные переменные."""
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Устанавливаем глобальные переменные
            global RABBITMQ_HOST, USERNAME, PASSWORD, VHOST, EXCHANGE_TYPE
            RABBITMQ_HOST = data["rabbitMQ"]["rabbitmq_api"]
            USERNAME = data["rabbitMQ"]["username"]
            PASSWORD = data["rabbitMQ"]["password"]
            VHOST = data["rabbitMQ"]["vhost"]
            EXCHANGE_TYPE = data["rabbitMQ"]["exchange_type"]
            
            # Явно указываем конкретную ноду
            #RABBITMQ_HOST = "rabbit@rabbitmq-3"  # или IP-адрес ноды
            
            return data
        else:
            print(f"Ошибка получения конфигурации: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при получении конфигурации: {e}")
        return None
    
url_config = "http://192.168.1.160:5050/data/json"
data = get_config(url_config)
instruments = str(data["instruments"]["instruments"]).split(",")
print(instruments)
for i in instruments:
    print(f"\nОбработка инструмента: {i}")
    # Создаём exchange
    if create_exchange_pika(i):
        # Создаём очереди
        create_queue_pika(i, i + "_bars")
        create_queue_pika(i, i + "_ord")