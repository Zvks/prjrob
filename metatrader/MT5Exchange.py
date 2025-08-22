import configparser
import MetaTrader5 as mt5
#from rabbit_MQ_rest import rabbitMQrest
import os
from datetime import datetime

class MT5Exchange:
    def __init__(self, config_path='C:\\Users\\user\\AppData\\Roaming\\MetaQuotes\\Terminal\\D0E8209F77C8CF37AD8BF550E51FF075\\MQL5\\Files\\config.ini'):
        """
        Инициализация класса MTExchange. Инициализация MetaTrader 5.      
        :param config_path: Путь к файлу конфигурации.
        """
        self.config_path = config_path
        self.config = configparser.ConfigParser(interpolation=None)
        self.rabbit_mq = None
        if not mt5.initialize():
            raise Exception(f"initialize() failed, error code = {mt5.last_error()}")
        
    def __symbol_exists(self, symbol):
        timeframe = mt5.TIMEFRAME_M5
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
        
        if rates is None or len(rates) == 0:
            print(f"Нет данных по свечам для {symbol}")
            return False  # просто возвращаем False

        last_candle_datetime = datetime.fromtimestamp(rates[0]['time'])
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f"Не удалось получить тик для {symbol}")
            return False

        server_datetime = datetime.fromtimestamp(tick.time)
        time_diff = server_datetime - last_candle_datetime
        diff_seconds = time_diff.total_seconds()

        return diff_seconds <= 300.0

    def create_config(self):
        """
        Создание и сохранение файла конфигурации.
        """
        # Получаем информацию об аккаунте
        account_info = mt5.account_info()
        if account_info is None:
            raise Exception("Ошибка получения информации об аккаунте")
        
        login = account_info.login
        server = account_info.server
        password = "@5PcRbGf"

        # Создаем секцию authorization
        self.config['authorization'] = {
            'login': str(login),
            'password': password,
            'server': server,
        }

        # Создаем секцию rabbitMQ
        self.config['rabbitMQ'] = {
            'rabbitmq_api': 'http://192.168.1.206:15671',
            'username': 'guest',
            'password': 'guest',
            'vhost': '%2F',
            'exchange_type': 'direct'
        }

        # Получаем список символов с USD
        symbols = mt5.symbols_get("*USD*")
        if symbols is None:
            raise Exception(f"Не удалось получить символы: {mt5.last_error()}")
        
        symbol_names = []
        for s in symbols:
            if self.__symbol_exists(s.name):
                symbol_names.append(s.name) 
                

        self.config['instruments'] = {'instruments': ','.join(symbol_names)}

        # Сохраняем конфигурацию в файл
        with open(self.config_path, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        return True

    def read_config_ini_to_json(self):
        """
        Считывает .ini файл и возвращает его содержимое в виде словаря.

        :param file_path: путь к .ini файлу
        :return: словарь с данными из .ini файла
        """
        config = configparser.ConfigParser(interpolation=None)
        config.read(self.config_path, encoding='utf-8')

        config_dict = {}
        for section in config.sections():
            config_dict[section] = {}
            for key, value in config.items(section):
                config_dict[section][key] = value

        self.config_dict = config_dict
        return config_dict
    
    def check_config_exists(self):
        """
        Проверяет, существует ли конфигурационный файл.
        :param config_path: Путь к конфигурационному файлу 
        :return: True, если файл существует, иначе False
        """
        return os.path.isfile(self.config_path)