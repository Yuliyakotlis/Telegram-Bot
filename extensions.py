import json
import requests
from config import keys


class ConvertionException(Exception):
    pass


class CurrencyConvecter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_str = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f"Валюта '{quote}' не найдена.\n\nСписок доступных валют: /values")

        try:
            base_str = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f"Валюта '{base}' не найдена.\n\nСписок доступных валют: /values")

        if quote == base:
            raise ConvertionException("Невозможно конвертировать одинаковые валюты.")

        try:
            amount = float(amount)
            if amount < 1:
                raise ValueError
        except ValueError:
            raise ConvertionException(f"Указано неверное количество валюты: '{amount}'.")


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_str}&tsyms={base_str}')
        total_base = json.loads(r.content)[keys[base.lower()]]
        return float(total_base) * amount
