import os
from datetime import datetime, timedelta

import pandas as pd

from external_api import currency_conversion


def working_with_transactions_period(request_time: str, period: str) -> object:
    """Считывает данные из файла и фильтрует их, заменяет записи на более удобные (суммы в валюте на рубли)"""

    path_file = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + 'operations.xlsx'
    try:
        df = pd.read_excel(path_file).iloc[:, [0, 2, 3, 4, 5, 8, 9, 11]]
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return []

    request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S")
    # Определение нижней границы поиска в зависимости от периода
    match period.upper():
        case 'M' | 'М':  # Учет алфавита
            request_time_start = request_time_end.replace(day=1, hour=0, minute=0, second=0)
        case 'W':
            request_time_start = request_time_end - timedelta(weeks=1)
        case 'Y':
            request_time_start = request_time_end.replace(day=1, month=1, hour=0, minute=0, second=0)
        case 'ALL':
            request_time_start = pd.to_datetime(df['Дата операции']).min()

    # Фильтрация списка транзакций
    df = df.loc[
        (pd.to_datetime(df['Дата операции'], dayfirst=True) <= request_time_end) &
        (pd.to_datetime(df['Дата операции'], dayfirst=True) >= request_time_start) &
        (df['Номер карты'].notnull()) &
        (df['Статус'].isin(['OK']))
        ]
    # Замена записей номеров карт в датафрейме
    df['Номер карты'] = df['Номер карты'].astype(str).apply(lambda x: x[-4:])

    # Замена сумм в валюте на рубли в датафрейме
    exchange_rates = {currency: currency_conversion(currency) for currency in df['Валюта операции'].unique()}


    df['Сумма операции'] = df.apply(lambda row: row['Сумма операции'] * exchange_rates[row['Валюта операции']], axis=1)
    df['Кэшбэк'] = df.apply(lambda row: row['Кэшбэк'] * exchange_rates[row['Валюта операции']], axis=1)


    return df
