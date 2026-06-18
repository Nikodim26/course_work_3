import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

from external_api import currency_conversion


def top_transaction_record(card_numbers, types_of_currencies, categories, financial_transactions):
    """Формирует список топовых транзакций в рублях"""

    top_transactions = []
    for card_number in card_numbers:
        for currency in types_of_currencies:
            for categori in categories:
                df = financial_transactions.loc[
                    (financial_transactions["Категория"] == categori) &
                    (financial_transactions['Номер карты'] == card_number) &
                    (financial_transactions["Валюта операции"] == currency)
                    ]
                if not df.empty:
                    amount_max = df['Сумма операции'].min()

                    top_transactions_df = df.loc[df['Сумма операции'] == amount_max]
                    date = str(top_transactions_df.iloc[0, 0])
                    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")

                    top_transactions.append(
                        {
                            "date": date,
                            "amount": abs(round(float(amount_max * currency_conversion(currency)), 2)),
                            "category": categori,
                            "description": str(top_transactions_df.iloc[0, 6])
                        }
                    )

    top_transactions = sorted(top_transactions, key=lambda x: x["amount"], reverse=True)[:5]

    return top_transactions


def recording_card_numbers(card_numbers, types_of_currencies, financial_transactions):
    """Формирует список карт"""

    cards = []
    for card_number in card_numbers:
        for currency in types_of_currencies:
            df = financial_transactions.loc[
                (financial_transactions['Номер карты'] == card_number) &
                (financial_transactions["Валюта операции"] == currency)
                ]
            if not df.empty:
                amount_of_expenses = abs(df['Сумма операции'].sum())
                total_spent=round(float(amount_of_expenses * currency_conversion(currency)), 2)
                cards.append(
                    {
                        "last_digits": card_number[1:],
                        "total_spent": total_spent,
                        "cashback": round(float(total_spent / 100), 2),
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

    return stocks


def determination_of_the_settlement_period(dates, request_time, range_requested):

    if range_requested.upper() == 'M':
        request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S").date()
        request_time_start = request_time_end - timedelta(days=request_time_end.day - 1)

    if range_requested.upper() == 'W':
        request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S").date()
        request_time_start = request_time_end - timedelta(days=request_time_end.day - 1)

    return request_time_start, request_time_start
