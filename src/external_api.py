import logging

import requests

logger = logging.getLogger(__name__)


def currency_conversion(currencies: list) -> dict:
    """Принимает на вход тип валюты и возвращает курс в рублях. Формирует словарь курсов валют."""

    try:
        for i in range(3):
            logger.info(f'Делаю запрос - {i + 1} попытка')
            response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            if response.status_code == 200:
                logger.info(f'Ответ получен: код {response.status_code}')
                break

        if response.status_code != 200:
            logger.error(f'Не получилось: код: {response.status_code}')
            print("Нет связи с БД. Конвертация невозможна")
            return {}
    except Exception as e:
        print(e)

    currency_base = {currency: response.json()["Valute"][currency.upper()]['Value'] if currency.upper() != 'RUB' else 1
                     for currency in currencies}
    logger.info('Создана база курсов валют')
    return currency_base
