import json
import os

from reading_the_database import working_with_transactions_period
from utils import record_exchange_rates, stock_quote_search


def working_with_transactions_events(request_time: str, period="m"):
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

    # Траты по 7 категориям
    main = []
    top_expenses = 0
    for i in range(7 if len(category_dictionary) >= 7 else len(category_dictionary)):
        main.append(
            {
                "category": category_dictionary[i][0],
                "amount": round(abs(category_dictionary[i][1]), 2)
            }
        )
        top_expenses += abs(category_dictionary[i][1])

    # Остальные траты
    main.append(
        {
            "category": "Остальное",
            "amount": round(total_amount_expenses - top_expenses, 2)
        }
    )
    category_dictionary = dict(category_dictionary)

    # Траты наличными и переводами
    transfers_and_cash = [
        {
            "category": "Наличные",
            "amount": round(abs(category_dictionary.get("Наличные", 0)), 2)
        },
        {
            "category": "Переводы",
            "amount": round(abs(category_dictionary.get("Переводы", 0)), 2)
        }
    ]
    transfers_and_cash = sorted(transfers_and_cash, key=lambda x: x["amount"], reverse=True)

    main_income = []
    for category in category_dictionary_income:
        main_income.append(
            {
                "category": category[0],
                "amount": round(abs(category[1]), 2)
            }
        )

    income = {
        "total_amount": round(total_amount_receipts, 2),
        "main": main_income
    }

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
            "main": main,
            'transfers_and_cash': transfers_and_cash,
            'income': income,
            "currency_rates": record_exchange_rates(user_currencies),
            "stock_prices": stock_quote_search(user_stocks)
        }
    }

    return json_str
