import requests


def currency_conversion(currency: str)->float:
    """Принимает на вход тип валюты и возвращает курс в рублях"""

    try:
        for i in range(3):
            response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            if response.status_code == 200:
                break

        if response.status_code != 200:
            raise Exception("Нет связи с БД. Конвертация невозможна")
    except Exception as e:
        print(e)
    return response.json()["Valute"][currency.upper()]["Value"] if currency.upper() !='RUB' else 1