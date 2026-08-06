import json
import logging
from pathlib import Path
from typing import Any

from day_phase import determining_the_phase_of_the_day
from reading_the_database import working_with_transactions_period
from utils import recording_card_numbers
from utils import recording_exchange_rates
from utils import recording_stock_quotes
from utils import top_transaction_record

logger = logging.getLogger(__name__)


def working_with_transactions(request_time: str, period: str = "m") -> dict[str, str | Any]:
    """Функция делает выборки и распечатку транзакций по заданному периоду относительно заданной даты"""

    # Чтение данных и их фильтрация
    financial_transactions, currency_base = working_with_transactions_period(request_time, period)

    financial_transactions = financial_transactions.loc[financial_transactions["Сумма платежа"] < 0]

    # Извлечение данных из отфильтрованного файла
    card_numbers = financial_transactions["Номер карты"].unique()

    # Чтение файла с заготовками
    data_path = Path(__file__).resolve().parent.parent / "user_settings.json"
    with open(data_path, "r") as f:
        data = json.load(f)
        user_currencies = data["user_currencies"]
        user_stocks = data["user_stocks"]

    logger.info("Формирую JSON-запись")
    # Формирование JSON
    json_dict = {
        "greeting": determining_the_phase_of_the_day(),
        "cards": recording_card_numbers(card_numbers, financial_transactions),
        "top_transactions": top_transaction_record(financial_transactions),
        "currency_rates": recording_exchange_rates(user_currencies, currency_base),
        "stock_prices": recording_stock_quotes(user_stocks, currency_base),
    }
    logger.info("JSON-запись сформирована")

    return json_dict


if __name__ == "__main__":
    b = working_with_transactions("2018-05-28 12:49:53")
    print(type(b))
    a = [i for i in b.keys()]
    print(a)
