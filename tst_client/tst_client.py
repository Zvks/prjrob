import requests
import json
import logging


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('client.log', encoding='utf-8'),
        logging.StreamHandler()  # Также выводим в консоль
    ]
)

logger = logging.getLogger(__name__)

# Базовый URL сервера
BASE_URL = "http://192.168.1.205:5000"

def main():
    logger.info("Клиент для тестирования сервера Flask")
    logger.info("-" * 40)
    
    try:
        # GET запрос к главной странице
        logger.info("1. GET запрос к главной странице:")
        response = requests.get(f"{BASE_URL}/")
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        logger.info("")
        
        # GET запрос к API данных
        logger.info("2. GET запрос к /api/data:")
        response = requests.get(f"{BASE_URL}/api/data")
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        logger.info("")
        
        # GET запрос с параметрами
        logger.info("3. GET запрос к пользователю с ID 123:")
        response = requests.get(f"{BASE_URL}/api/user/123")
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        logger.info("")
        
        # POST запрос
        logger.info("4. POST запрос к /api/echo:")
        data_to_send = {
            "message": "Привет от клиента!",
            "timestamp": "2024-01-01 12:00:00"
        }
        response = requests.post(
            f"{BASE_URL}/api/echo",
            json=data_to_send
        )
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Ответ: {response.json()}")
        logger.info("")
        
        logger.info("Все запросы выполнены успешно")
        
    except requests.exceptions.ConnectionError:
        logger.error("Ошибка подключения к серверу. Убедитесь, что сервер запущен.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при выполнении запроса: {e}")
    except json.JSONDecodeError:
        logger.error("Ошибка при разборе JSON ответа")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")

if __name__ == '__main__':
    while (True):
        main()