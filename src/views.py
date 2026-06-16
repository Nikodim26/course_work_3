import json
from datetime import datetime, timedelta

import pandas as pd

from day_phase import determining_the_phase_of_the_day
from reading_the_database import about_financial_transactions_xlsx


def working_with_transactions(request_time: str):
    """Функция делает выборки и распечатку транзакций по текущему месяцу относительно заданной даты"""

    pd.set_option('display.max_columns', None)

    request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S").date()
    request_time_start = request_time_end - timedelta(days=request_time_end.day - 1)

    financial_transactions = about_financial_transactions_xlsx('operations.xlsx').iloc[:, [1, 2, 3, 4, 5, 9,11]]

    financial_transactions['Дата платежа'] = pd.to_datetime(financial_transactions['Дата платежа'])
    financial_transactions = financial_transactions.loc[
        (financial_transactions['Дата платежа'] <= pd.to_datetime(request_time_end)) &
        (financial_transactions['Дата платежа'] >= pd.to_datetime(request_time_start)) &
        (financial_transactions['Номер карты'].notnull()) &
        (financial_transactions['Статус'].isin(['OK']))]

    card_numbers = financial_transactions['Номер карты'].unique()
    types_of_currencies = financial_transactions['Валюта операции'].unique()
    categories = dict(financial_transactions["Категория"].value_counts().nlargest(5))

    top_transactions = []
    for categori in categories.keys():
        categori_df = financial_transactions.loc[
            (financial_transactions["Категория"] == categori)]

        amount_max = categori_df.loc[categori_df['Сумма операции'] < 0, 'Сумма операции'].min()
        top_transactions_df = categori_df.loc[categori_df['Сумма операции'] == amount_max]
        date = str(top_transactions_df.iloc[0, 0])
        date=datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")

        a = 1
        top_transactions.append(
            {
                "date": date,
                "amount": abs(round(float(amount_max), 2)),
                "category": categori,
                "description": str(top_transactions_df.iloc[0, 6])
            }
        )

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
                "top_transactions":top_transactions
                }


    return json_str


# working_with_transactions('2019-05-20 12:49:53')

print(working_with_transactions('2019-05-20 12:49:53'))

## Запчасти
# request_time_start = request_time[:8] + '01'
# request_time_end = request_time[:10]
# (financial_transactions['Дата платежа'].between(request_time_start, request_time_end)) &
