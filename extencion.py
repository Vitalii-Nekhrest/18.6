import requests
import json
from config import keys
# Использование библиотек requests и json согласно пунк.6,7; и все классы в файле extensions.py пунк 12 задания
class APIException(Exception):
# Класс APIException с текстом ошибки согласно пункта 8 задания
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # Статический метод get_price согласно пункта 10 задания
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюти {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = ((json.loads(r.content)[keys[base]]) * amount)
        return total_base