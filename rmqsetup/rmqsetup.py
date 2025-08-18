import requests
import json
import pika
import sys


def get_config(url):
    # Выполняем GET-запрос
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим JSON
        data = response.json()
        # Выводим красиво отформатированный JSON
        return data
    else:
        print(f"Ошибка: {response.status_code}")
        return response.status_code

def create_rabbitmq_connection(config):
    """Создает подключение к RabbitMQ"""
    try:
        credentials = pika.PlainCredentials(
            config['rabbitMQ']['username'],
            config['rabbitMQ']['password']
        )
        
        parameters = pika.ConnectionParameters(
            host=config['rabbitMQ']['rabbitmq_api'].split('/')[2].split(':')[0],  # извлекаем хост из URL
            port=5672,  # стандартный порт RabbitMQ
            virtual_host='/',  # декодируем %2F в /
            credentials=credentials
        )
        
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        return connection, channel
    except Exception as e:
        print(f"Ошибка подключения к RabbitMQ: {e}")
        sys.exit(1)

def create_exchange_and_queues(channel, instrument):
    """Создает exchange и очереди для инструмента"""
    try:
        # Создаем exchange с названием инструмента
        channel.exchange_declare(
            exchange=instrument,
            exchange_type='direct',
            durable=True
        )
        print(f"Создан exchange: {instrument}")
        
        # Создаем очередь для ордеров
        order_queue = f"{instrument}_ord"
        channel.queue_declare(queue=order_queue, durable=True)
        channel.queue_bind(exchange=instrument, queue=order_queue, routing_key=order_queue)
        print(f"Создана очередь: {order_queue}")
        
        # Создаем очередь для баров
        bar_queue = f"{instrument}_bar"
        channel.queue_declare(queue=bar_queue, durable=True)
        channel.queue_bind(exchange=instrument, queue=bar_queue, routing_key=bar_queue)
        print(f"Создана очередь: {bar_queue}")
        
    except Exception as e:
        print(f"Ошибка при создании exchange и очередей для {instrument}: {e}")

def main():
    # URL REST API endpoint
    url = "http://localhost:5050/data/json"  # Пример URL
    config = get_config(url)
    
    # Получаем список инструментов
    instruments_str = config['instruments']['instruments']
    instruments = [inst.strip() for inst in instruments_str.split(',') if inst.strip()]
    
    if not instruments:
        print("Ошибка: Не найдено инструментов для обработки")
        sys.exit(1)
    
    print(f"Найдено инструментов: {len(instruments)}")
    
    # Подключаемся к RabbitMQ
    connection, channel = create_rabbitmq_connection(config)
    
    try:
        # Создаем exchange и очереди для каждого инструмента
        for instrument in instruments:
            create_exchange_and_queues(channel, instrument)
            print("-" * 40)
        
        print("Все exchange и очереди успешно созданы!")
        
    except Exception as e:
        print(f"Ошибка при создании компонентов RabbitMQ: {e}")
    finally:
        # Закрываем соединение
        connection.close()

if __name__ == "__main__":
    main()