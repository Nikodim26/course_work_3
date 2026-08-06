import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def receiving_cashback_data() -> list[dict]:
    """Считывает данные из файла, фильтрует и формирует список транзакций"""

    data_path = Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"

    try:
        df = pd.read_excel(data_path)[["Дата платежа", "Кэшбэк", "Статус", "Категория", "Номер карты"]]
    except Exception as e:
        logger.error(e)
        return []

    df = df.loc[(df["Кэшбэк"].notnull()) & (df["Номер карты"].notnull()) & (df["Статус"].isin(["OK"]))]

    return df.loc[:, ["Дата платежа", "Кэшбэк", "Категория"]].to_dict(orient="records")


def determination_of_cashback_categories(transactions: list[dict], year: str, month: str) -> str:
    """Формирует JSON по выгоде категорий кешбэка"""

    logger.info("Список транзакций и время анализа получены")
    dt_search = datetime.strftime(datetime(int(year), int(month), 1, 0, 0, 0), "%m.%Y")

    fn = lambda x: datetime.strftime(datetime.strptime(x, "%d.%m.%Y"), "%m.%Y")

    categories = set(i["Категория"] for i in transactions if fn(i["Дата платежа"]) == dt_search)

    cashback_by_category = {}
    for category in categories:
        cashback_list = [
            float(i["Кэшбэк"])
            for i in transactions
            if i["Категория"] == category and fn(i["Дата платежа"]) == dt_search
        ]
        cashback_by_category[category] = round(sum(cashback_list))

    cashback_list_sorted = dict(sorted(cashback_by_category.items(), key=lambda x: x[1], reverse=True))
    logger.info("JSON-запись сформирована")

    return json.dumps(cashback_list_sorted, indent=4, ensure_ascii=False)
