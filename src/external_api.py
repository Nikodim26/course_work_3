import requests


def currency_conversion(currencies: list) -> dict:
    """Принимает на вход тип валюты и возвращает курс в рублях"""

    try:
        for i in range(3):
            response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            if response.status_code == 200:
                break

        if response.status_code != 200:
            print("Нет связи с БД. Конвертация невозможна")
            return {}
    except Exception as e:
        print(e)

    currency_base = {currency: response.json()["Valute"][currency.upper()]['Value'] if currency.upper() != 'RUB' else 1
                     for currency in currencies}

    return currency_base
