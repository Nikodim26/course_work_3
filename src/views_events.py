import json
import os
from typing import Any

from reading_the_database import working_with_transactions_period
from utils import recording_stock_quotes, recording_exchange_rates, post_by_category, transfer_recording_and_cache, \
    record_of_replenishments


def working_with_transactions_events(request_time: str, period: str = "m") -> dict[str, str | Any]:
    """Функция делает выборки и распечатку транзакций по заданному периоду относительно заданной даты"""

    # Чтение данных и их фильтрация
    df = working_with_transactions_period(request_time, period)

    total_amount_expenses = abs(df.query('`Сумма операции` < 0')['Сумма операции'].sum())  # общие затраты
    total_amount_receipts = df.query('`Сумма операции` > 0')['Сумма операции'].sum()  # общие

    category_dictionary_income = df[df["Сумма операции"] > 0].groupby("Категория")["Сумма операции"].sum()
    category_dictionary_income = sorted(category_dictionary_income.items(), key=lambda item: item[1])

    # затраты по категориям
    category_dictionary = df[df["Сумма операции"] < 0].groupby("Категория")["Сумма операции"].sum()
    category_dictionary = sorted(category_dictionary.items(), key=lambda item: item[1])

    # Чтение файла с заготовками
    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + 'user_settings.json'
    with open(path, 'r') as f:
        data = json.load(f)
        user_currencies = data['user_currencies']
        user_stocks = data['user_stocks']

    # Формирование JSON
    json_str = {
        "expenses": {
            "total_amount": round(total_amount_expenses, 2),
            "main": post_by_category(category_dictionary, total_amount_expenses),
            'transfers_and_cash': transfer_recording_and_cache(category_dictionary),
            'income': record_of_replenishments(category_dictionary_income, total_amount_receipts, df),
            "currency_rates": recording_exchange_rates(user_currencies),
            "stock_prices": recording_stock_quotes(user_stocks)
        }
    }

    return json_str
