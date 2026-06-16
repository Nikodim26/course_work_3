from datetime import datetime, timedelta

import pandas as pd

from day_phase import determining_the_phase_of_the_day
from reading_the_database import about_financial_transactions_xlsx
from utils import top_transaction_record, recording_card_numbers


def working_with_transactions(request_time: str):
    """Функция делает выборки и распечатку транзакций по текущему месяцу относительно заданной даты"""

    pd.options.display.expand_frame_repr = False

    # Фильтрование информации из файла
    request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S").date()
    request_time_start = request_time_end - timedelta(days=request_time_end.day - 1)

    financial_transactions = about_financial_transactions_xlsx('operations.xlsx').iloc[:, [1, 2, 3, 4, 5, 9, 11]]

    financial_transactions['Дата платежа'] = pd.to_datetime(financial_transactions['Дата платежа'], dayfirst=True)
    financial_transactions = financial_transactions.loc[
        (financial_transactions['Дата платежа'] <= pd.to_datetime(request_time_end)) &
        (financial_transactions['Дата платежа'] >= pd.to_datetime(request_time_start)) &
        (financial_transactions['Номер карты'].notnull()) &
        (financial_transactions['Сумма операции'] < 0) &
        (financial_transactions['Статус'].isin(['OK']))]

    # Извлечение данных из отфильтрованного файла
    card_numbers = financial_transactions['Номер карты'].unique()
    types_of_currencies = financial_transactions['Валюта операции'].unique()
    categories = financial_transactions["Категория"].unique()

    # Формирование JSON
    json_str = {
        "greeting": determining_the_phase_of_the_day(),
        "cards": recording_card_numbers(card_numbers,types_of_currencies,financial_transactions),
        "top_transactions": top_transaction_record(card_numbers, types_of_currencies,categories,financial_transactions)
    }

    return json_str


print(working_with_transactions('2018-01-31 12:49:53'))