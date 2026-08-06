import json
import logging
import time
from pathlib import Path

from reports import receiving_a_dataframe_with_transactions
from reports import spending_by_category
from services import determination_of_cashback_categories
from services import receiving_cashback_data
from views import working_with_transactions
from views_events import working_with_transactions_events

BASE_DIR = Path(__file__).resolve().parent.parent

log_path = BASE_DIR / "logs" / "main.log"
logging.basicConfig(
    level=logging.INFO,
    filemode="w",
    encoding="UTF8",
    filename=log_path,
    datefmt="%d-%m-%Y в %H:%M:%S",
    format="%(levelname)s: %(asctime)s %(name)s %(message)s",
)
logger = logging.getLogger("main")


def print_json(data, file):
    logger.info("Начал выводить информацию в JSON-файл, для контроля")
    json_path = BASE_DIR / "data" / f"{file}"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info("Закончил выводить информацию в JSON-файл, для контроля")


def main(data_time: str, period: str) -> None:
    """Функция выдает JSON строки для фронтенда 'Главная' и 'События'"""

    # Строка для фронтенда 'Главная'
    logger.info('Для "Главная" поехали')
    json_for_main = working_with_transactions(data_time)
    print_json(json_for_main, "1.json")
    logger.info('Конец для "Главная"')

    # Строка для фронтенда 'События'
    logger.info("Ожидание периода допуска к API")
    time.sleep(60)
    logger.info('Для "События" поехали')
    json_for_events = working_with_transactions_events(data_time, period)
    print_json(json_for_events, "2.json")
    logger.info('Конец для "События"')

    print(determination_of_cashback_categories(receiving_cashback_data(), "2020", "11"))

    spending_by_category(receiving_a_dataframe_with_transactions(), "Супермаркеты", "28.05.2019")


if __name__ == "__main__":
    main("2018-05-28 12:49:53", "M")
