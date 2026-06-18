import json
import os

from day_phase import determining_the_phase_of_the_day
from reading_the_database import working_with_transactions_period
from utils import top_transaction_record, recording_card_numbers, record_exchange_rates, stock_quote_search


def working_with_transactions(request_time: str, period="m"):
    """Функция делает выборки и распечатку транзакций по заданному периоду относительно заданной даты"""

    # Чтение данных и их фильтрация
    financial_transactions = working_with_transactions_period(request_time, period)

    # Извлечение данных из отфильтрованного файла
    card_numbers = financial_transactions['Номер карты'].unique()
    types_of_currencies = financial_transactions['Валюта операции'].unique()
    categories = financial_transactions["Категория"].unique()

    # Чтение файла с заготовками
    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + 'user_settings.json'
    with open(path, 'r') as f:
        data = json.load(f)
        user_currencies = data['user_currencies']
        user_stocks = data['user_stocks']

    # Формирование JSON
    json_str = {
        "greeting": determining_the_phase_of_the_day(),
        "cards": recording_card_numbers(card_numbers, types_of_currencies, financial_transactions),
        "top_transactions": top_transaction_record(card_numbers, types_of_currencies, categories,
                                                   financial_transactions),
        "currency_rates": record_exchange_rates(user_currencies),
        "stock_prices": stock_quote_search(user_stocks)
    }

    return json_str
