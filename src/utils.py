import logging
import os
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def top_transaction_record(card_numbers: list, categories: list, financial_transactions: object) -> object:
    """Формирует список топовых транзакций по картам и категориям"""

    top_transactions = []
    logger.info('Формирую топ транзакций')
    for card_number in card_numbers:
        for categori in categories:
            df = financial_transactions.loc[
                (financial_transactions["Категория"] == categori) &
                (financial_transactions['Номер карты'] == card_number)
                ]
            if not df.empty:
                amount_max = df['Сумма операции'].min()

                top_transactions_df = df.loc[df['Сумма операции'] == amount_max]
                date = datetime.strptime(top_transactions_df.iloc[0, 0], "%d.%m.%Y %H:%M:%S")

                top_transactions.append(
                    {
                        "date": datetime.strftime(date, "%d.%m.%Y"),
                        "amount": abs(round(amount_max, 2)),
                        "category": categori,
                        "description": str(top_transactions_df.iloc[0, 6])
                    }
                )

    top_transactions = sorted(top_transactions, key=lambda x: x["amount"], reverse=True)[:5]
    logger.info('Сформирован топ транзакций')
    return top_transactions


def recording_card_numbers(card_numbers: list, financial_transactions: object) -> list[dict]:
    """Формирует список банковских карт"""

    cards = []
    logger.info('Формирую список банковских карт')
    for card_number in card_numbers:
        df = financial_transactions.loc[(financial_transactions['Номер карты'] == card_number)]
        if not df.empty:
            amount_of_expenses = abs(df['Сумма операции'].sum())
            cards.append(
                {
                    "last_digits": card_number,
                    "total_spent": round(amount_of_expenses, 2),
                    "cashback": round(amount_of_expenses / 100, 2)
                }
            )

    logger.info('Сформирован список банковских карт')
    return cards




def recording_exchange_rates(types_of_currencies: list, currency_base: dict) -> list[dict]:
    """Формирует запись о курсах валют"""

    exchange_rates = []
    logger.info('Формирую запись о курсах валют')
    for currency in types_of_currencies:
        exchange_rates.append(
            {
                "currency": currency,
                "rate": round(currency_base[currency], 2)
            }
        )
    logger.info('Сформирована запись о курсах валют')
    return exchange_rates


def recording_stock_quotes(user_stocks: list, currency_base: dict) -> list[dict]:
    """Формирует список котировок акций"""

    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    stocks = []
    logger.info('Формирую список котировок акций')
    for stock in user_stocks:
        url1 = f"https://api.massive.com/v3/reference/tickers/{stock}?apiKey={API_KEY}"
        url2 = f"https://api.massive.com/v2/aggs/ticker/{stock}/prev?apiKey={API_KEY}"

        try:
            for i in range(3):
                logger.info(f'Делаю запросы по акциям {stock}- {i + 1} попытка')
                response1 = requests.get(url1)
                response2 = requests.get(url2)
                if response1.status_code == 200 and response2.status_code == 200:
                    logger.info(f'Получена информация по акциям {stock}')
                    break

            if response1.status_code != 200 or response2.status_code != 200:
                logger.error('Нет связи с БД. Информация по акциям недоступна.')
                print("Нет связи с БД. Информация по акциям недоступна.")
                return []

        except Exception as e:
            logger.error(f'Ошибка {e}')
            print(e)

        currency = response1.json().get('results').get("currency_name")
        if currency:
            price = response2.json().get('results')[0].get('c') * currency_base[currency.upper()]
            if price:
                stocks.append(
                    {
                        "stock": stock,
                        "price": round(price, 2)
                    }
                )

    logger.info('Сформирована запись о котировках акций')

    return sorted(stocks, key=lambda x: x["price"], reverse=True)


def post_by_category(category_dictionary: list, total_amount_expenses: float) -> list:
    """Формирует список трат по категориям"""

    # Траты по 7 категориям
    main = []
    logger.info('Формирую список трат по категориям')
    top_expenses = 0
    for i in range(7 if len(category_dictionary) >= 7 else len(category_dictionary)):
        main.append(
            {
                "category": category_dictionary[i][0],
                "amount": round(abs(category_dictionary[i][1]), 2)
            }
        )

        top_expenses += abs(category_dictionary[i][1])

    # Остальные траты
    main.append(
        {
            "category": "Остальное",
            "amount": round(total_amount_expenses - top_expenses, 2)
        }
    )
    logger.info('Сформирован список трат по категориям')

    return main


def transfer_recording_and_cache(category_dictionary: dict) -> list:
    """Формирует список трат по типу"""

    # Траты наличными и переводами
    logger.info('Формирую список трат по типу')
    transfers_and_cash = [
        {
            "category": "Наличные",
            "amount": round(abs(category_dictionary.get("Наличные", 0)), 2)
        },
        {
            "category": "Переводы",
            "amount": round(abs(category_dictionary.get("Переводы", 0)), 2)
        }
    ]
    logger.info('Сформирован список трат по типу')

    return sorted(transfers_and_cash, key=lambda x: x["amount"], reverse=True)


def record_of_replenishments(category_dictionary_income, total_amount_receipts, df) -> dict[str, list[Any] | Any]:
    """Формирует запись пополнений"""

    main_income = []
    logger.info('Формирую запись о пополнениях')
    for category in category_dictionary_income:
        main_income.append(
            {
                "category": category[0],
                "amount": round(abs(category[1]), 2)
            }
        )

    cashback_amount = df.loc[df['Кэшбэк'].notnull()]['Кэшбэк'].sum()
    main_income.append(
        {
            "category": "Кэшбэк",
            "amount": round(cashback_amount, 2)
        }
    )

    income = {
        "total_amount": round(total_amount_receipts, 2),
        "main": main_income

    }
    logger.info('Сформирована запись о пополнениях')

    return income
