import json
import logging
from pathlib import Path
from typing import Any

from reading_the_database import working_with_transactions_period
from utils import recording_exchange_rates, recording_stock_quotes

logger = logging.getLogger(__name__)


def working_with_transactions_events(
    request_time: str, period: str
) -> dict[str, str | Any]:
    """Функция делает выборки и распечатку транзакций по заданному периоду относительно заданной даты"""

    # Чтение данных и их фильтрация
    df, currency_base = working_with_transactions_period(request_time, period)

    total_amount_expenses = abs(
        df.query("`Сумма операции` < 0")["Сумма операции"].sum()
    )  # общие затраты
    total_amount_receipts = abs(
        df.query("`Сумма операции` > 0")["Сумма операции"].sum()
    )  # общие поступления

    category_dictionary = (
        df[df["Сумма операции"] < 0]
        .groupby("Категория")["Сумма операции"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )
    main = [
        {"category": name, "amount": round(amount)}
        for name, amount in category_dictionary.head(7).items()
    ]

    other_amount = (
        round(category_dictionary.iloc[7:].sum()) if len(category_dictionary) > 7 else 0
    )
    if other_amount > 0:
        main.append({"category": "Остальное", "amount": other_amount})

    transfers_and_cash = sorted(
        [
            {
                "category": "Наличные",
                "amount": round(abs(category_dictionary.get("Наличные", 0))),
            },
            {
                "category": "Переводы",
                "amount": round(abs(category_dictionary.get("Переводы", 0))),
            },
        ],
        key=lambda x: x["amount"],
        reverse=True,
    )

    category_dictionary_income = (
        df[df["Сумма операции"] > 0]
        .groupby("Категория")["Сумма операции"]
        .sum()
        .sort_values(ascending=False)
    )

    # Чтение файла с заготовками
    data_path = Path(__file__).resolve().parent.parent / "user_settings.json"
    with open(data_path, "r") as f:
        data = json.load(f)
        user_currencies = data["user_currencies"]
        user_stocks = data["user_stocks"]

    logger.info("Формирую JSON-запись")
    # Формирование JSON
    json_str = {
        "expenses": {
            "total_amount": round(total_amount_expenses),
            "main": main,
            "transfers_and_cash": transfers_and_cash,
        },
        "income": {
            "total_amount": round(total_amount_receipts),
            "main": [
                {"category": name, "amount": round(amount)}
                for name, amount in category_dictionary_income.items()
            ],
        },
        "currency_rates": recording_exchange_rates(user_currencies, currency_base),
        "stock_prices": recording_stock_quotes(user_stocks, currency_base),
    }

    logger.info("JSON-запись сформирована")
    return json_str
