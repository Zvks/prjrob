import MetaTrader5 as mt5

class Ord:
    def __init__(self, account, password, server):
        self.account = account
        self.password = password
        self.server = server
        # Инициализируем подключение к терминалу, если ещё не инициализировано
        if not mt5.initialize():
            print("Ошибка инициализации MT5")
        if not mt5.login(account = account, password = password, server = server):
            print("Ошибка входа в счет MT5")
        
    def __ord_sell(self, symbol = "EURUSD", lot = 0.1):
        mt5.symbol_select(symbol, True)
        tick = mt5.symbol_info_tick(symbol)
        price = tick.ask
        request_s = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price * 1.05,
        "tp": price * 0.85,
        "deviation": 20,
        "magic": self.account,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK
        }
        # === Отправка ордера ===
        result = mt5.order_send(request_s)

        # === Проверка результата ===
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return (f"Ошибка при отправке ордера: {result.retcode}")
        else:
            return ("Ордер успешно исполнен")

    def __ord_buy(self, symbol = "EURUSD", lot = 0.1):
        mt5.symbol_select(symbol, True)
        tick = mt5.symbol_info_tick(symbol)
        price = tick.ask
        request_b = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price * 0.95,
            "tp": price * 1.25,
            "deviation": 20,
            "magic": self.account,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }
        # === Отправка ордера ===
        result = mt5.order_send(request_b)

        # === Проверка результата ===
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return (f"Ошибка при отправке ордера: {result.retcode}")
        else:
            return ("Ордер успешно исполнен")
        
    def __pending_buy_limit(self, symbol="EURUSD", lot=0.1, price=None, sl_ratio=0.95, tp_ratio=1.25):
        mt5.symbol_select(symbol, True)
        if price is None:
            tick = mt5.symbol_info_tick(symbol)
            price = tick.bid * 0.98  # Ниже текущей цены для BUY LIMIT
        
        # Для BUY LIMIT цена должна быть ниже текущей цены
        # SL должен быть ниже цены, TP выше цены
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY_LIMIT,  # Исправлено: BUY_LIMIT
            "price": price,
            "sl": price * sl_ratio,  # Для BUY_LIMIT SL должен быть ниже цены
            "tp": price * tp_ratio,  # Для BUY_LIMIT TP должен быть выше цены
            "deviation": 20,
            "magic": self.account,
            "comment": "python script BUY LIMIT",  # Исправлено комментарий
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(result)
            return f"Ошибка при выставлении Buy Limit: {result.retcode} | {result.comment}"
        else:
            return f"Buy Limit успешно выставлен по цене {price}"
        
    def __pending_sell_limit(self, symbol="EURUSD", lot=0.1, price=None, sl_ratio=1.05, tp_ratio=0.85):
        """
        Выставление отложенного ордера Sell Limit (продажа дороже текущей цены)
        """
        mt5.symbol_select(symbol, True)
        if price is None:
            tick = mt5.symbol_info_tick(symbol)
            price = tick.bid * 1.02  # Выше текущей цены для SELL LIMIT

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL_LIMIT,  # Исправлено: SELL_LIMIT
            "price": price,
            "sl": price * sl_ratio,  # Для SELL_LIMIT SL должен быть выше цены
            "tp": price * tp_ratio,  # Для SELL_LIMIT TP должен быть ниже цены
            "deviation": 20,
            "magic": self.account,
            "comment": "python script SELL LIMIT",  # Исправлено комментарий
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(result)
            return f"Ошибка при выставлении Sell Limit: {result.retcode} | {result.comment}"
        else:
            return f"Sell Limit успешно выставлен по цене {price}"

    def __pending_buy_stop(self, symbol="EURUSD", lot=0.1, price=None, sl_ratio=0.95, tp_ratio=1.25):
        """
        Выставление отложенного ордера Buy Stop (покупка выше текущей — например, при пробое)
        """
        mt5.symbol_select(symbol, True)
        if price is None:
            tick = mt5.symbol_info_tick(symbol)
            price = tick.ask * 1.02  # Выше текущей цены

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY_STOP,
            "price": price,
            "sl": price * sl_ratio,
            "tp": price * tp_ratio,
            "deviation": 20,
            "magic": self.account,
            "comment": "python script BUY STOP",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return f"Ошибка при выставлении Buy Stop: {result.retcode} | {result.comment}"
        else:
            return f"Buy Stop успешно выставлен по цене {price}"

    def __pending_sell_stop(self, symbol="EURUSD", lot=0.1, price=None, sl_ratio=1.05, tp_ratio=0.85):
        """
        Выставление отложенного ордера Sell Stop (продажа ниже текущей)
        """
        mt5.symbol_select(symbol, True)
        if price is None:
            tick = mt5.symbol_info_tick(symbol)
            price = tick.bid * 0.98  # Ниже текущей цены

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL_STOP,
            "price": price,
            "sl": price * sl_ratio,
            "tp": price * tp_ratio,
            "deviation": 20,
            "magic": self.account,
            "comment": "python script SELL STOP",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return f"Ошибка при выставлении Sell Stop: {result.retcode} | {result.comment}"
        else:
            return f"Sell Stop успешно выставлен по цене {price}"

    def __close_position_by_ticket(self, ticket):
        # Получаем позицию по тикету
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            print(f"Позиция с тикетом {ticket} не найдена")
            return False
        
        position = position[0]
        
        # Подготавливаем запрос на закрытие
        symbol = position.symbol
        volume = position.volume
        position_type = position.type
        
        # Определяем тип ордера для закрытия (противоположный текущей позиции)
        if position_type == mt5.ORDER_TYPE_BUY:
            order_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
        else:
            order_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
        
        # Создаем запрос на закрытие
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "deviation": 10,
            "magic": position.magic,
            "comment": "Closed by python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }
        
        # Отправляем ордер на закрытие
        result = mt5.order_send(close_request)
        
        # Проверяем результат выполнения
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Ошибка при закрытии позиции {ticket}: {result.comment}")
            return False
        
        print(f"Позиция {ticket} успешно закрыта")
        return True

    def __close_positions(self, filter_type="all", filter_symbol="all"):
        # Получаем все открытые позиции
        positions = mt5.positions_get()
        
        if len(positions) == 0:
            print("Нет открытых позиций")
            return True
        
        for position in positions:
            # Применяем фильтры
            type_ok = (filter_type == "all" or 
                    (filter_type == "buy" and position.type == mt5.ORDER_TYPE_BUY) or
                    (filter_type == "sell" and position.type == mt5.ORDER_TYPE_SELL))
            
            symbol_ok = (filter_symbol == "all" or position.symbol == filter_symbol)
            
            if type_ok and symbol_ok:
                self.close_position_by_ticket(position.ticket)
        return True

    def __update_order(self, ticket, down_max=2, up_max=30):
        position = mt5.positions_get(ticket=ticket)
        if not position:
            print(f"Сделка {ticket} не найдена")
            return False

        position = position[0]
        symbol = position.symbol
        price = position.price_open
        deal_type = position.type

        # Получаем точность цены и минимальный шаг
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f"Ошибка: не удалось получить информацию по символу {symbol}")
            return False

        digits = symbol_info.digits
        point = 10 ** (-digits)  # 0.0001 для 4 знаков, 0.01 для 2 знаков

        # Рассчитываем новые SL/TP в ПРОЦЕНТАХ (down_max=2% -> 0.02)
        if deal_type == mt5.ORDER_TYPE_BUY:
            new_sl = price * (1 - down_max / 100)
            new_tp = price * (1 + up_max / 100)
            # Проверяем, чтобы SL был ниже цены
            new_sl = min(new_sl, price - 10 * point)
        elif deal_type == mt5.ORDER_TYPE_SELL:
            new_sl = price * (1 + down_max / 100)
            new_tp = price * (1 - up_max / 100)
            # Проверяем, чтобы SL был выше цены
            new_sl = max(new_sl, price + 10 * point)
        else:
            print("Неизвестный тип сделки")
            return False

        # Округляем до нужного кол-ва знаков
        new_sl = round(new_sl, digits)
        new_tp = round(new_tp, digits)

        # Проверяем, чтобы SL/TP не были слишком близко к цене
        if deal_type == mt5.ORDER_TYPE_BUY and new_sl >= price:
            new_sl = price - 10 * point
        elif deal_type == mt5.ORDER_TYPE_SELL and new_sl <= price:
            new_sl = price + 10 * point

        # Отправляем запрос
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "position": ticket,
            "sl": new_sl,
            "tp": new_tp,
            "deviation": 10,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Ошибка обновления: {result.comment}. Проверьте уровни SL/TP.")
            return False

        print(f"Сделка {ticket} обновлена: SL={new_sl}, TP={new_tp}")
        return True

    def __update_all_orders(self, filter_type="all", filter_symbol="all", down_max=2, up_max=30):
        # Получаем все открытые позиции
        positions = mt5.positions_get()
        
        if len(positions) == 0:
            print("Нет открытых позиций")
            return True
        
        for position in positions:
            # Применяем фильтры
            type_ok = (filter_type == "all" or 
                    (filter_type == "buy" and position.type == mt5.ORDER_TYPE_BUY) or
                    (filter_type == "sell" and position.type == mt5.ORDER_TYPE_SELL))
            
            symbol_ok = (filter_symbol == "all" or position.symbol == filter_symbol)
            
            if type_ok and symbol_ok:
                self.update_order(position.ticket, down_max = down_max, up_max = up_max)
        return True
    
    def __cancel_pending_order_by_ticket(self, ticket):
        """
        Отменяет (удаляет) отложенный ордер по ticket.
        """
        pending_orders = mt5.orders_get(ticket=ticket)
        if pending_orders is None or len(pending_orders) == 0:
            print(f"Отложенный ордер с тикетом {ticket} не найден")
            return False

        order = pending_orders[0]
        symbol = order.symbol

        # Подготовка запроса на удаление (через модификацию объема в 0)
        # Но MT5 требует отправить ордер с action=TRADE_ACTION_DELETE для отложенных
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,  # Удаление отложенного ордера
            "order": ticket,                    # Номер ордера (ticket)
            "symbol": symbol,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Ошибка при удалении ордера {ticket}: {result.comment}")
            return False

        print(f"Отложенный ордер {ticket} успешно удалён")
        return True


    def __cancel_pending_orders(self, filter_type="all", filter_symbol="all"):
        """
        Массовая отмена отложенных ордеров по фильтру.
        filter_type: "all", "buy_limit", "sell_limit", "buy_stop", "sell_stop"
        filter_symbol: "all" или конкретный символ, например "EURUSD"
        """
        orders = mt5.orders_get()
        if orders is None or len(orders) == 0:
            print("Нет активных отложенных ордеров")
            return True

        type_map = {
            "buy_limit": mt5.ORDER_TYPE_BUY_LIMIT,
            "sell_limit": mt5.ORDER_TYPE_SELL_LIMIT,
            "buy_stop": mt5.ORDER_TYPE_BUY_STOP,
            "sell_stop": mt5.ORDER_TYPE_SELL_STOP,
        }

        for order in orders:
            # Проверяем тип
            if filter_type != "all":
                expected_type = type_map.get(filter_type.lower())
                if expected_type is None:
                    print(f"Неизвестный тип фильтра: {filter_type}")
                    continue
                if order.type != expected_type:
                    continue

            # Проверяем символ
            if filter_symbol != "all" and order.symbol != filter_symbol:
                continue

            self.cancel_pending_order_by_ticket(order.ticket)

        return True


    def __update_pending_order(self, ticket, new_price=None, down_max=2, up_max=30):
        """
        Обновляет отложенный ордер: цену, SL и TP.
        Если new_price не указан, оставляет текущую.
        SL и TP устанавливаются как отклонение в процентах от первоначальной цены входа.
        """
        orders = mt5.orders_get(ticket=ticket)
        if not orders:
            print(f"Отложенный ордер {ticket} не найден")
            return False

        order = orders[0]
        symbol = order.symbol
        current_price = order.price_open
        order_type = order.type
        digits = mt5.symbol_info(symbol).digits
        point = 10 ** (-digits)

        # Если новая цена не задана — оставляем старую
        price = new_price if new_price is not None else current_price
        price = round(price, digits)

        # Рассчитываем SL и TP в зависимости от типа ордера
        if order_type == mt5.ORDER_TYPE_BUY_LIMIT:
            # BUY LIMIT: покупаем дешевле => SL ещё ниже, TP выше
            sl = price * (1 - down_max / 100)
            tp = price * (1 + up_max / 100)
            sl = min(sl, price - 10 * point)  # SL должен быть ниже
        elif order_type == mt5.ORDER_TYPE_BUY_STOP:
            # BUY STOP: покупаем дороже => SL ниже цены, TP выше
            sl = price * (1 - down_max / 100)
            tp = price * (1 + up_max / 100)
            sl = min(sl, price - 10 * point)
        elif order_type == mt5.ORDER_TYPE_SELL_LIMIT:
            # SELL LIMIT: продаём дороже => SL выше, TP ниже
            sl = price * (1 + down_max / 100)
            tp = price * (1 - up_max / 100)
            sl = max(sl, price + 10 * point)
        elif order_type == mt5.ORDER_TYPE_SELL_STOP:
            # SELL STOP: продаём ещё дороже => SL выше, TP ниже
            sl = price * (1 + down_max / 100)
            tp = price * (1 - up_max / 100)
            sl = max(sl, price + 10 * point)
        else:
            print(f"Неподдерживаемый тип ордера: {order_type}")
            return False

        # Округляем
        sl = round(sl, digits)
        tp = round(tp, digits)

        # Проверка, чтобы SL не был слишком близко
        if order_type in [mt5.ORDER_TYPE_BUY_LIMIT, mt5.ORDER_TYPE_BUY_STOP] and sl >= price:
            sl = price - 10 * point
        elif order_type in [mt5.ORDER_TYPE_SELL_LIMIT, mt5.ORDER_TYPE_SELL_STOP] and sl <= price:
            sl = price + 10 * point

        # Формируем запрос на модификацию
        request = {
            "action": mt5.TRADE_ACTION_MODIFY,
            "order": ticket,
            "symbol": symbol,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 10,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Ошибка при обновлении ордера {ticket}: {result.comment}")
            return False

        print(f"Отложенный ордер {ticket} обновлён: Price={price}, SL={sl}, TP={tp}")
        return True


    def __update_all_pending_orders(self, filter_type="all", filter_symbol="all", new_price=None, down_max=2, up_max=30):
        """
        Массовое обновление всех отложенных ордеров по фильтрам.
        Можно указать новую цену (одну для всех), или оставить None — тогда сохранится старая.
        """
        orders = mt5.orders_get()
        if not orders:
            print("Нет активных отложенных ордеров")
            return True

        valid_types = {
            "buy_limit": mt5.ORDER_TYPE_BUY_LIMIT,
            "sell_limit": mt5.ORDER_TYPE_SELL_LIMIT,
            "buy_stop": mt5.ORDER_TYPE_BUY_STOP,
            "sell_stop": mt5.ORDER_TYPE_SELL_STOP,
        }

        for order in orders:
            # Фильтр по типу
            if filter_type != "all":
                expected_type = valid_types.get(filter_type.lower())
                if expected_type is None:
                    print(f"Неизвестный тип фильтра: {filter_type}")
                    continue
                if order.type != expected_type:
                    continue

            # Фильтр по символу
            if filter_symbol != "all" and order.symbol != filter_symbol:
                continue

            # Обновляем каждый ордер
            self.update_pending_order(order.ticket, new_price=new_price, down_max=down_max, up_max=up_max)

        return True

    def __get_ord(self):
        return mt5.orders_get()
    
    def __get_positions(self):
        return mt5.positions_get()

        # Public methods
    def createOrder(self, order_type, symbol="EURUSD", lot=0.1, price=None, sl_ratio=None, tp_ratio=None):
        """
        Public method to create any type of order
        Args:
            order_type (str): "buy", "sell", "buy_limit", "sell_limit", "buy_stop", "sell_stop"
            symbol (str): Trading symbol
            lot (float): Volume in lots
            price (float): Price for pending orders (optional)
            sl_ratio (float): Stop Loss ratio (e.g., 0.95 for 5% below)
            tp_ratio (float): Take Profit ratio (e.g., 1.25 for 25% above)
        Returns:
            str: Result message
        """
        # Default SL/TP ratios if not provided
        if sl_ratio is None:
            sl_ratio = 0.95 if "buy" in order_type else 1.05
        if tp_ratio is None:
            tp_ratio = 1.25 if "buy" in order_type else 0.85
            
        if order_type == "buy":
            return self.__ord_buy(symbol=symbol, lot=lot)
        elif order_type == "sell":
            return self.__ord_sell(symbol=symbol, lot=lot)
        elif order_type == "buy_limit":
            return self.__pending_buy_limit(symbol=symbol, lot=lot, price=price, 
                                          sl_ratio=sl_ratio, tp_ratio=tp_ratio)
        elif order_type == "sell_limit":
            return self.__pending_sell_limit(symbol=symbol, lot=lot, price=price, 
                                           sl_ratio=sl_ratio, tp_ratio=tp_ratio)
        elif order_type == "buy_stop":
            return self.__pending_buy_stop(symbol=symbol, lot=lot, price=price, 
                                        sl_ratio=sl_ratio, tp_ratio=tp_ratio)
        elif order_type == "sell_stop":
            return self.__pending_sell_stop(symbol=symbol, lot=lot, price=price, 
                                         sl_ratio=sl_ratio, tp_ratio=tp_ratio)
        else:
            return "Invalid order type"

    def updateOrder(self, ticket=None, order_type=None, filter_type="all", filter_symbol="all", 
                   new_price=None, down_max=2, up_max=30):
        """
        Public method to update orders (both positions and pending orders)
        Args:
            ticket (int): Specific order/position ticket to update
            order_type (str): "position" or "pending" - what to update
            filter_type (str): "all", "buy", "sell", "buy_limit", etc.
            filter_symbol (str): "all" or specific symbol
            new_price (float): New price for pending orders
            down_max (float): Max drawdown percentage for SL
            up_max (float): Max profit percentage for TP
        Returns:
            bool: True if successful, False otherwise
        """
        if ticket is not None:
            if order_type == "position":
                return self.__update_order(ticket, down_max=down_max, up_max=up_max)
            elif order_type == "pending":
                return self.__update_pending_order(ticket, new_price=new_price, 
                                                 down_max=down_max, up_max=up_max)
            else:
                print("Must specify 'position' or 'pending' when updating by ticket")
                return False
        else:
            if order_type == "position":
                return self.__update_all_orders(filter_type=filter_type, 
                                             filter_symbol=filter_symbol,
                                             down_max=down_max, up_max=up_max)
            elif order_type == "pending":
                return self.__update_all_pending_orders(filter_type=filter_type,
                                                      filter_symbol=filter_symbol,
                                                      new_price=new_price,
                                                      down_max=down_max,
                                                      up_max=up_max)
            else:
                print("Must specify 'position' or 'pending' for mass update")
                return False

    def closeOrder(self, ticket=None, order_type=None, filter_type="all", filter_symbol="all"):
        """
        Public method to close orders/positions
        Args:
            ticket (int): Specific order/position ticket to close
            order_type (str): "position" or "pending" - what to close
            filter_type (str): "all", "buy", "sell", etc.
            filter_symbol (str): "all" or specific symbol
        Returns:
            bool: True if successful, False otherwise
        """
        if ticket is not None:
            if order_type == "position":
                return self.__close_position_by_ticket(ticket)
            elif order_type == "pending":
                return self.__cancel_pending_order_by_ticket(ticket)
            else:
                print("Must specify 'position' or 'pending' when closing by ticket")
                return False
        else:
            if order_type == "position":
                return self.__close_positions(filter_type=filter_type, 
                                          filter_symbol=filter_symbol)
            elif order_type == "pending":
                return self.__cancel_pending_orders(filter_type=filter_type,
                                                  filter_symbol=filter_symbol)
            else:
                print("Must specify 'position' or 'pending' for mass close")
                return False

    def readOrder(self, order_type="all", filter_type="all", filter_symbol="all"):
        """
        Public method to read orders/positions
        Args:
            order_type (str): "position", "pending", or "all"
            filter_type (str): "all", "buy", "sell", etc.
            filter_symbol (str): "all" or specific symbol
        Returns:
            list: List of orders/positions or None if error
        """
        result = []
        
        if order_type in ["all", "position"]:
            positions = self.__get_positions()
            if positions is not None:
                for pos in positions:
                    type_ok = (filter_type == "all" or 
                             (filter_type == "buy" and pos.type == mt5.ORDER_TYPE_BUY) or
                             (filter_type == "sell" and pos.type == mt5.ORDER_TYPE_SELL))
                    symbol_ok = (filter_symbol == "all" or pos.symbol == filter_symbol)
                    if type_ok and symbol_ok:
                        result.append(pos)
        
        if order_type in ["all", "pending"]:
            orders = self.__get_ord()
            if orders is not None:
                type_map = {
                    "buy_limit": mt5.ORDER_TYPE_BUY_LIMIT,
                    "sell_limit": mt5.ORDER_TYPE_SELL_LIMIT,
                    "buy_stop": mt5.ORDER_TYPE_BUY_STOP,
                    "sell_stop": mt5.ORDER_TYPE_SELL_STOP,
                }
                for order in orders:
                    type_ok = True
                    if filter_type != "all":
                        expected_type = type_map.get(filter_type.lower())
                        if expected_type is None:
                            continue
                        type_ok = (order.type == expected_type)
                    
                    symbol_ok = (filter_symbol == "all" or order.symbol == filter_symbol)
                    
                    if type_ok and symbol_ok:
                        result.append(order)
        
        return result if len(result) > 0 else None

    def shutdown(self):
        """
        Properly shutdown MT5 connection
        """
        mt5.shutdown()

