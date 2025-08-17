import logging
import datetime

import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

message = "ta.py"

# Бесконечный цикл
while True:
    # Получаем текущее время
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Выводим сообщение в лог
    logging.info(f"{message}, Time: {current_time}")
    # Задержка на 1 секунду
    time.sleep(1)