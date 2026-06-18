import os
from datetime import datetime, timedelta

import pandas as pd


def working_with_transactions_period(request_time, period) -> list[dict]:
    """Определяет период поиска """

    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + 'operations.xlsx'
    try:
        df = pd.read_excel(path).iloc[:, [0, 2, 3, 4, 5, 9, 11]]
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return []

    request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S")

    match period.upper():
        case 'M' | 'М':  # Учет алфавита
            request_time_start = request_time_end.replace(day=1, hour=0, minute=0, second=0)
        case 'W':
            request_time_start = request_time_end - timedelta(weeks=1)
        case 'Y':
            request_time_start = request_time_end.replace(day=1, month=1, hour=0, minute=0, second=0)
        case 'ALL':
            request_time_start = df['Дата операции'].min()

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

    # Фильтрация списка транзакций
    df = df.loc[
        (df['Дата операции'] <= pd.to_datetime(request_time_end)) &
        (df['Дата операции'] >= pd.to_datetime(request_time_start)) &
        (df['Номер карты'].notnull()) &
        (df['Сумма операции'] < 0) &
        (df['Статус'].isin(['OK']))]

    return df
