import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def top_transaction_record(financial_transactions) -> list[dict]:
    """Формирует список топовых транзакций по сумме платежа"""

    top_transactions = []
    logger.info("Формирую топ транзакций")

    df = financial_transactions.loc[(financial_transactions["Сумма платежа"] < 0)].nsmallest(5, "Сумма платежа")

    for _, row in df.iterrows():
        date = datetime.strptime(str(row["Дата операции"]), "%d.%m.%Y %H:%M:%S")
        top_transactions.append(
            {
                "date": date.strftime("%d.%m.%Y"),
                "amount": abs(round(row["Сумма платежа"], 2)),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    logger.info("Сформирован топ транзакций")
    return top_transactions


def recording_card_numbers(card_numbers: list, financial_transactions: pd.DataFrame) -> list[dict]:
    """Формирует список банковских карт"""

    cards = []
    logger.info("Формирую список банковских карт")
    for card_number in card_numbers:
        df = financial_transactions.loc[(financial_transactions["Номер карты"] == card_number)]
        if not df.empty:
            amount_of_expenses = abs(df["Сумма операции"].sum())
            cards.append(
                {
                    "last_digits": card_number,
                    "total_spent": round(amount_of_expenses, 2),
                    "cashback": round(amount_of_expenses / 100, 2),
                }
            )

    logger.info("Сформирован список банковских карт")
    return cards


def recording_exchange_rates(types_of_currencies: list, currency_base: dict) -> list[dict]:
    """Формирует запись о курсах валют"""

    exchange_rates = []
    logger.info("Формирую запись о курсах валют")
    for currency in types_of_currencies:
        exchange_rates.append({"currency": currency, "rate": round(currency_base[currency], 2)})

    logger.info("Сформирована запись о курсах валют")
    return exchange_rates


def recording_stock_quotes(user_stocks: list, currency_base: dict) -> list[dict]:
    """Формирует список котировок акций"""

    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    stocks = []
    logger.info("Формирую список котировок акций")
    for stock in user_stocks:
        url1 = f"https://api.massive.com/v3/reference/tickers/{stock}?apiKey={API_KEY}"
        url2 = f"https://api.massive.com/v2/aggs/ticker/{stock}/prev?apiKey={API_KEY}"

        try:
            for i in range(3):
                logger.info(f"Делаю запросы по акциям {stock}- {i + 1} попытка")
                response1 = requests.get(url1)
                response2 = requests.get(url2)
                if response1.status_code == 200 and response2.status_code == 200:
                    logger.info(f"Получена информация по акциям {stock}")
                    break

            if response1.status_code != 200 or response2.status_code != 200:
                logger.error("Нет связи с БД. Информация по акциям недоступна.")
                continue

            currency = response1.json().get("results").get("currency_name")
            price = response2.json().get("results")[0].get("c") * currency_base[currency.upper()]
            stocks.append({"stock": stock, "price": round(price, 2)})
        except Exception as e:
            logger.error(f"Ошибка {e}")

    logger.info("Сформирована запись о котировках акций")
    return sorted(stocks, key=lambda x: x["price"], reverse=True)
