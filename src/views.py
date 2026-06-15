from datetime import datetime, timedelta

import pandas as pd

from reading_the_database import about_financial_transactions_xlsx


def working_with_transactions(request_time: str, period: int) -> None:
    """Функция делает выборки и распечатку транзакций по текущему месяцу относительно заданной даты"""

    request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S").date()
    request_time_start = request_time_end - timedelta(weeks=period * 4, days=request_time_end.day - 1)

    financial_transactions = about_financial_transactions_xlsx('operations.xlsx').iloc[:, 1:6]
    financial_transactions['Дата платежа'] = pd.to_datetime(financial_transactions['Дата платежа'])

    financial_transactions = financial_transactions.loc[
        (financial_transactions['Дата платежа'] <= pd.to_datetime(request_time_end)) &
        (financial_transactions['Дата платежа'] >= pd.to_datetime(request_time_start)) &
        (financial_transactions['Номер карты'].notnull()) &
        (financial_transactions['Статус'].isin(['OK']))]

    card_numbers = financial_transactions['Номер карты'].unique()
    types_of_currencies = financial_transactions['Валюта операции'].unique()

    for card_number in card_numbers:
        for currency in types_of_currencies:
            transaction = financial_transactions.loc[
                (financial_transactions['Номер карты'] == card_number) & (
                        financial_transactions["Валюта операции"] == currency)]

            amount_of_expenses = abs(transaction.loc[transaction['Сумма операции'] < 0, 'Сумма операции'].sum())

            print(f"""
            За период с {request_time_start} по {request_time_end}
            
            Номер карты: {card_number}
            Общие расходы: {round(amount_of_expenses, 2)} {currency}
            Kешбэк: {int(amount_of_expenses / 100)} {currency}
            """)

    # return printout

# print((working_with_transactions('2019-05-20 12:49:53')))

## Запчасти
# request_time_start = request_time[:8] + '01'
# request_time_end = request_time[:10]
# (financial_transactions['Дата платежа'].between(request_time_start, request_time_end)) &
