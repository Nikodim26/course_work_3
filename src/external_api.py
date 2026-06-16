import requests


def currency_conversion(currency: str):
    """Принимает на вход тип валюты и возвращает курс в рублях"""
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        if response.status_code != 200:
            raise ValueError("Failed to get currency rate")
    except Exception:
        print("Что-то, блин, не так, как хотелось бы")

    return response.json()["Valute"].get(currency)["Value"]

# currency_conversion('EUR')
