import logging
from pathlib import Path

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
    except Exception as e:
        logger.error(e)
        return None

    df = df.loc[(df['Номер карты'].notnull()) & (df['Статус'].isin(['OK']))]
    currency_base = currency_conversion(df['Валюта операции'].unique())  # Создание кэш курсов валют
    df = df.loc[df['Сумма платежа'] < 0]
    df['Сумма платежа'] = df.apply(lambda row: row['Сумма платежа'] * currency_base[row['Валюта операции']], axis=1)
    df = df.loc[:, ["Дата операции", "Сумма платежа", "Категория"]]

    return df


if __name__ == '__main__':
    receiving_a_dataframe_with_transactions()
