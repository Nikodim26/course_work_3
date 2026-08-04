import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
from pandas import DataFrame

from external_api import currency_conversion

logger = logging.getLogger(__name__)


def receiving_a_dataframe_with_transactions() -> DataFrame | None:
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


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    df = transactions

    if date:
        request_time_end = datetime.strptime(date, "%d.%m.%Y")
    else:
        request_time_end = datetime.now()

    request_time_start = request_time_end - timedelta(weeks=12)

    df = df.loc[
        (pd.to_datetime(df['Дата операции'], dayfirst=True) <= request_time_end) &
        (pd.to_datetime(df['Дата операции'], dayfirst=True) >= request_time_start) &
        (df['Категория'] == category)
        ]

    return df


if __name__ == '__main__':
    df=spending_by_category(receiving_a_dataframe_with_transactions(), 'Супермаркеты', '28.05.2019')
    # spending_by_category(receiving_a_dataframe_with_transactions(), 'Супермаркеты')

    data_path = Path(__file__).resolve().parent.parent / "data" / "df.txt"
    with open(data_path, 'w', encoding="utf-8") as f:
        f.write(df.to_string(index=False))

    data_path = Path(__file__).resolve().parent.parent / "data" / "df.xlsx"
    df.to_excel(data_path, index=False)