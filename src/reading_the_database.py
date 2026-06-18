import os
from datetime import datetime, timedelta

import pandas as pd


def about_financial_transactions(request_time, range_requested) -> list[dict]:
    """Принимает на вход путь до XLSX-файла и возвращает список словарей с данными о финансовых транзакциях"""

    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + 'operations.xlsx'
    request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S")

    try:
        df = pd.read_excel(path).iloc[:, [0, 2, 3, 4, 5, 9, 11]]
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return []

    # Перевод даты операции в другой формат
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

    match range_requested.upper():
        case 'M' | 'М':
            request_time_start = request_time_end.replace(day=1, hour=0, minute=0, second=0)
        case 'W':
            request_time_start = request_time_end - timedelta(weeks=1)
        case 'Y':
            request_time_start = request_time_end.replace(day=1, month=1, hour=0, minute=0, second=0)
        case 'ALL':
            request_time_start = df['Дата операции'].min()

    # Фильтрация списка транзакций
    df = df.loc[
        (df['Дата операции'] <= pd.to_datetime(request_time_end)) &
        (df['Дата операции'] >= pd.to_datetime(request_time_start)) &
        (df['Номер карты'].notnull()) &
        (df['Сумма операции'] < 0) &
        (df['Статус'].isin(['OK']))]

    return df
