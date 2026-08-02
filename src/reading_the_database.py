import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from external_api import currency_conversion

logger = logging.getLogger(__name__)


def working_with_transactions_period(request_time: str, period: str) -> object:
    """Считывает данные из файла и фильтрует их, заменяет записи на более удобные (суммы в валюте на рубли)"""

    data_path = Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"

    try:
        df = pd.read_excel(data_path)[[
            "Дата операции", "Номер карты", "Статус",
            "Сумма операции", "Валюта операции",
            "Сумма платежа", "Категория", "Описание"
        ]]

    except Exception as e:
        logger.error('Не удалось прочитать данные')
        return []

    logger.info('Данные получены. Выбраны интересующие позиции')
    currency_base = currency_conversion(df['Валюта операции'].unique())  # Создание кэш курсов валют
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

    logger.info('Определены временные границы поиска')
    # Фильтрация списка транзакций
    df = df.loc[
        (pd.to_datetime(df['Дата операции'], dayfirst=True) <= request_time_end) &
        (pd.to_datetime(df['Дата операции'], dayfirst=True) >= request_time_start) &
        (df['Номер карты'].notnull()) &
        (df['Статус'].isin(['OK']))
        ]
    # Замена записей номеров карт в датафрейме
    df['Номер карты'] = df['Номер карты'].apply(lambda x: x[-4:])

    # Замена сумм в валюте на рубли в датафрейме
    df['Сумма операции'] = df.apply(lambda row: row['Сумма операции'] * currency_base[row['Валюта операции']], axis=1)
    df['Сумма платежа'] = df.apply(lambda row: row['Сумма платежа'] * currency_base[row['Валюта операции']], axis=1)
    logger.info('Датафрейм отфильтрован')

    return df, currency_base
