import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from external_api import currency_conversion


def top_transaction_record(card_numbers, categories, financial_transactions):
    """Формирует список топовых транзакций в рублях"""

    top_transactions = []
    for card_number in card_numbers:
        for categori in categories:
            df = financial_transactions.loc[
                (financial_transactions["Категория"] == categori) &
                (financial_transactions['Номер карты'] == card_number)
                ]
            if not df.empty:
                amount_max = df['Сумма операции'].min()

                top_transactions_df = df.loc[df['Сумма операции'] == amount_max]
                date = datetime.strptime(top_transactions_df.iloc[0, 0],"%d.%m.%Y %H:%M:%S")

                top_transactions.append(
                    {
                        "date": datetime.strftime(date,"%d.%m.%Y"),
                        "amount": abs(round(amount_max, 2)),
                        "category": categori,
                        "description": str(top_transactions_df.iloc[0, 6])
                    }
                )

    top_transactions = sorted(top_transactions, key=lambda x: x["amount"], reverse=True)[:5]

    return top_transactions


def recording_card_numbers(card_numbers, financial_transactions):
    """Формирует список карт"""

    cards = []
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
    return cards


def record_exchange_rates(types_of_currencies):
    """Формирует запись о курсах валют"""

    exchange_rates = []
    for currency in types_of_currencies:
        if currency.upper != "RUB":
            exchange_rates.append(
                {
                    "currency": currency,
                    "rate": round(currency_conversion(currency), 2)
                }
            )

    return exchange_rates


def stock_quote_search(user_stocks):
    """Формирует список котировок акций"""

    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    stocks = []
    for stock in user_stocks:
        url1 = f"https://api.massive.com/v3/reference/tickers/{stock}?apiKey={API_KEY}"
        url2 = f"https://api.massive.com/v2/aggs/ticker/{stock}/prev?apiKey={API_KEY}"

        try:
            currency = dict(requests.get(url1).json())['results']["currency_name"]
            price = dict(requests.get(url2).json())['results'][0]['vw'] * currency_conversion(currency.upper())
        except Exception as e:
            print(e)

        stocks.append(
            {
                "stock": stock,

                "price": round(price, 2)
            }
        )

    return sorted(stocks,key=lambda x:x["price"],reverse=True)
