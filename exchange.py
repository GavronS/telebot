from typing import List, Any

import requests
import json
from config import excanges

payload = {}
headers= {
  "apikey": "OGptFdAzk6iCMgIIErUFWGxvIIeiM6Aw"
}

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = excanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = excanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if  base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')
        # try:
        #     amount = float(amount.replace(",", "."))
        # except ValueError:
        #     raise APIException(f'Не удалось обработать количество {amount}')
        url = (f"https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={amount}")
        r = requests.request("GET", url, headers=headers, data = payload)
        resp = json.loads(r.content)
        return resp['result']

# класс выдающий валюты в правильном склонении в зависимости от введенного
# количества валюты и результата конвертации
class Declination:
    @staticmethod
    def get_excanges(base, sym, amount, result):
        base = base.lower()
        sym = sym.lower()
        amount = int(amount)
        result = int(result)
        valute = []
        if base == 'доллар':
            if (amount%10 == 1 or amount%100 == 1 or amount%1000 ==1 or amount%10000 ==1):
                base = 'доллар'
            elif (amount%10 == 2 or amount%100 == 2 or amount%1000 ==2 or amount%10000 ==2):
                base = 'доллара'
            elif (amount % 10 == 3 or amount % 100 == 3 or amount % 1000 == 3 or amount % 10000 == 3):
                base = 'доллара'
            elif (amount % 10 == 4 or amount % 100 == 4 or amount % 1000 == 4 or amount % 10000 == 4):
                base = 'доллара'
            else:
                base = 'долларов'
        if base == 'рубль':
            if (amount % 10 == 1 or amount % 100 == 1 or amount % 1000 == 1 or amount % 10000 == 1):
                base = 'рубль'
            elif (amount % 10 == 2 or amount % 100 == 2 or amount % 1000 == 2 or amount % 10000 == 2):
                base = 'рубля'
            elif (amount % 10 == 3 or amount % 100 == 3 or amount % 1000 == 3 or amount % 10000 == 3):
                base = 'рубля'
            elif (amount % 10 == 4 or amount % 100 == 4 or amount % 1000 == 4 or amount % 10000 == 4):
                base = 'рубля'
            else:
                base = 'рублей'
        valute.append(base)

        if sym == 'доллар':
            if (result%10 == 1 or result%100 == 1 or result%1000 ==1 or result%10000 ==1):
                sym = 'доллар'
            elif (result%10 == 2 or result%100 == 2 or result%1000 ==2 or result%10000 ==2):
                sym = 'доллара'
            elif (result % 10 == 3 or result % 100 == 3 or result % 1000 == 3 or result % 10000 == 3):
                sym = 'доллара'
            elif (result % 10 == 4 or result % 100 == 4 or result % 1000 == 4 or result % 10000 == 4):
                sym = 'доллара'
            else:
                sym = 'долларов'
        if sym == 'рубль':
            if (result % 10 == 1 or result % 100 == 1 or result % 1000 == 1 or result % 10000 == 1):
                sym = 'рубль'
            elif (result % 10 == 2 or result % 100 == 2 or result % 1000 == 2 or result % 10000 == 2):
                sym = 'рубля'
            elif (result % 10 == 3 or result % 100 == 3 or result % 1000 == 3 or result % 10000 == 3):
                sym = 'рубля'
            elif (result % 10 == 4 or result % 100 == 4 or result % 1000 == 4 or result % 10000 == 4):
                sym = 'рубля'
            else:
                sym = 'рублей'
        valute.append(sym)
        return valute

