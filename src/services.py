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

    return df.loc[:, ["Дата платежа", "Кэшбэк", "Категория"]].to_dict(orient='records')


def determination_of_cashback_categories(transactions: list[dict], year: str, month: str) -> str:
    """Формирует JSON по выгоде категорий кешбэка"""

    dt_search = datetime.strftime(datetime(int(year), int(month), 1, 0, 0, 0), '%m.%Y')

    fn = lambda x: datetime.strftime(datetime.strptime(x, '%d.%m.%Y'), '%m.%Y')
    b = fn('30.12.2021')

    categories = set(i['Категория'] for i in transactions if fn(i["Дата платежа"]) == dt_search)

    cashback_by_category = {}
    for category in categories:
        cashback_list = [float(i['Кэшбэк']) for i in transactions if
                         i["Категория"] == category and fn(i["Дата платежа"]) == dt_search]

        cashback_by_category[category] = round(sum(cashback_list))
        cashback_list_sorted = dict(sorted(cashback_by_category.items(), key=lambda x: x[1], reverse=True))

    return json.dumps(cashback_list_sorted, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    print(receiving_cashback_data())
    print(determination_of_cashback_categories(receiving_cashback_data(), '2019', '5'))
