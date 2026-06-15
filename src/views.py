from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from day_phase import determining_the_phase_of_the_day
from reading_the_database import about_financial_transactions_xlsx


def working_with_transactions(request_time: str) -> list[Any]:
    """Функция делает выборки и распечатку транзакций по текущему месяцу относительно заданной даты"""

    request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S").date()
    request_time_start = request_time_end - timedelta(days=request_time_end.day - 1)

    financial_transactions = about_financial_transactions_xlsx('operations.xlsx').iloc[:, 1:6]
    financial_transactions['Дата платежа'] = pd.to_datetime(financial_transactions['Дата платежа'])

    financial_transactions = financial_transactions.loc[
        (financial_transactions['Дата платежа'] <= pd.to_datetime(request_time_end)) &
        (financial_transactions['Дата платежа'] >= pd.to_datetime(request_time_start)) &
        (financial_transactions['Номер карты'].notnull()) &
        (financial_transactions['Статус'].isin(['OK']))]

    card_numbers = financial_transactions['Номер карты'].unique()
    types_of_currencies = financial_transactions['Валюта операции'].unique()

    cards=[]
    for card_number in card_numbers:
        for currency in types_of_currencies:
            transaction = financial_transactions.loc[
                (financial_transactions['Номер карты'] == card_number) & (
                        financial_transactions["Валюта операции"] == currency)]

            amount_of_expenses = abs(transaction.loc[transaction['Сумма операции'] < 0, 'Сумма операции'].sum())

            cards.append(
                {
                "last_digits": card_number[1:],
                "total_spent": round(float(amount_of_expenses),2),
                "cashback": round(float(amount_of_expenses / 100),2)
                }
            )

    json_str = {
                "greeting": determining_the_phase_of_the_day(),
                "cards": cards,
                "top_transactions":

                }
    #     Номер карты: {card_number}
    # Общие
    # расходы: {round(amount_of_expenses, 2)}
    # {currency}
    # Kешбэк: {int(amount_of_expenses / 100)}
    # {currency}
    # """)


    return json_str


print(working_with_transactions('2019-05-20 12:49:53'))

## Запчасти
# request_time_start = request_time[:8] + '01'
# request_time_end = request_time[:10]
# (financial_transactions['Дата платежа'].between(request_time_start, request_time_end)) &
