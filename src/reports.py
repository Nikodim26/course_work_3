import logging
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Optional

import pandas as pd

from external_api import currency_conversion

logger = logging.getLogger(__name__)


def receiving_a_dataframe_with_transactions() -> pd.DataFrame | None:
    """Формирует датафрейм транзакций для создания отчета"""

    data_path = Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"

    try:
        df = pd.read_excel(data_path)[
            ["Дата операции", "Статус", "Валюта операции", "Сумма платежа", "Категория", "Номер карты"]]
        logger.info('Получены данные')
    except Exception as e:
        logger.error(e)
        return None

    df = df.loc[(df['Номер карты'].notnull()) & (df['Статус'].isin(['OK']))]
    currency_base = currency_conversion(df['Валюта операции'].unique())  # Создание кэш курсов валют
    df = df.loc[df['Сумма платежа'] < 0]
    df['Сумма платежа'] = df.apply(lambda row: row['Сумма платежа'] * currency_base[row['Валюта операции']], axis=1)
    df = df.loc[:, ["Дата операции", "Сумма платежа", "Категория"]]

    logger.info('Датафрейм отфильтрован')

    return df


def my_decorator(filename: str):
    """Дополняет работу функции записью результатов в файл"""

    def wrapper(func):
        @wraps(func)
        def print_in_file(*args, **kwargs):

            try:
                data_path = Path(__file__).resolve().parent.parent / "data" / filename
                func(*args, **kwargs).to_excel(data_path, index=False)
            except Exception as e:
                logger.error(e)

        return print_in_file

    return wrapper


@my_decorator("df.xlsx")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    if date:
        request_time_end = datetime.strptime(date, "%d.%m.%Y")
    else:
        request_time_end = datetime.now()

    request_time_start = request_time_end - timedelta(weeks=12)

    df = transactions.loc[
        (pd.to_datetime(transactions['Дата операции'], dayfirst=True) <= request_time_end) &
        (pd.to_datetime(transactions['Дата операции'], dayfirst=True) >= request_time_start) &
        (transactions['Категория'] == category)
        ]

    return df
