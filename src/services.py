import json
from datetime import datetime
from pathlib import Path

import pandas as pd


def receiving_cashback_data() -> list[dict]:
    """Считывает данные из файла, фильтрует и формирует список словарей"""

    data_path = Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"

    try:
        df = pd.read_excel(data_path)[["Дата платежа", "Кэшбэк", "Статус", "Категория", "Номер карты"]]
    except Exception as e:
        return []

    df = df.loc[(df['Кэшбэк'].notnull()) & (df['Номер карты'].notnull()) & (df['Статус'].isin(['OK']))]
    # df['Дата платежа'] = df['Дата платежа'].apply(lambda x: x[-7:])

    return df.loc[:, ["Дата платежа", "Кэшбэк", "Категория"]].to_dict(orient='records')


transactions = receiving_cashback_data()


def determination_of_cashback_categories(transactions: list[dict], year: str, month: str) -> str:
    """Формирует JSON по выгоде категорий кешбэка"""

    dt = datetime(int(year), int(month), 0, 0, 0, 0)
    dt=datetime.strptime(dt, '%Y-%m-%d')

    categories = set(i['Категория'] for i in transactions if i["Дата платежа"] == f'0{month}.{year}')

    cashback_by_category = {}
    for category in categories:
        cashback_list = [float(i['Кэшбэк']) for i in transactions if
             i["Категория"] == category and i["Дата платежа"] == f'0{month}.{year}']

        cashback_by_category[category] = round(sum(cashback_list))
        cashback_list_sorted = dict(sorted(cashback_by_category.items(), key=lambda x: x[1], reverse=True))


    return json.dumps(cashback_list_sorted, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    print(receiving_cashback_data())
    print(determination_of_cashback_categories(receiving_cashback_data(), '2019', '5'))
