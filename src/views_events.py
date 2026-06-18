import json
import os

from day_phase import determining_the_phase_of_the_day
from reading_the_database import working_with_transactions_period
from utils import top_transaction_record, recording_card_numbers, record_exchange_rates, stock_quote_search


def working_with_transactions_events(request_time: str, period="m"):
    """Функция делает выборки и распечатку транзакций по заданному периоду относительно заданной даты"""

    # Чтение данных и их фильтрация
    df = working_with_transactions_period(request_time, period)

    total_amount_expenses = abs(df.query('`Сумма операции` < 0')['Сумма операции'].sum())# общие затраты
    total_amount_receipts = df.query('`Сумма операции` > 0')['Сумма операции'].sum()# общие постуаления

    # затраты по категориям
    category_dictionary = df[df["Сумма операции"] < 0].groupby("Категория")["Сумма операции"].sum()
    category_dictionary = sorted(category_dictionary.items(), key=lambda item: item[1])

    main=[]
    counter =0
    for i in range(1):
        main.append(
            {
                "category": category_dictionary[i][0],
                "amount": round(abs(category_dictionary[i][1]),2)
            }
        )


    # Формирование JSON
    json_str = {
        "expenses": {
            "total_amount": round(total_amount_expenses, 2),
            "main": []
        }
    }

    return json_str
