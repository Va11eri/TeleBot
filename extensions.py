import requests
import json
from config2 import keys
from config2 import TOKEN


class APIException(Exception):
    pass
class CryptoConvector:
    @staticmethod
    def convert(quote: str, base: str, amount:str):
        if quote == base:
            raise APIException('Sorry, you entered similar currencies!')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Failed to process currency {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Failed to process currency {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Failed to process quantity {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * float(amount)
        return total_base
