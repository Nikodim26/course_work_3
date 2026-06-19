import json
import logging
import os
import time

from views import working_with_transactions

from views_events import working_with_transactions_events

path = os.path.dirname(os.path.dirname(__file__)) + "\\logs\\main.log"
logging.basicConfig(
    level=logging.INFO, filemode="w", encoding="UTF8", filename=path, datefmt="%d-%m-%Y в %H:%M:%S",
    format="%(levelname)s: %(asctime)s %(name)s %(message)s"
)
logger = logging.getLogger("main")


def main(data_time: str) -> None:
    """Функция выдает JSON строки для фронтенда 'Главная' и 'События'"""

    # Строка для фронтенда 'Главная'
    logger.info('Для "Главная" поехали')
    json_for_main = working_with_transactions(data_time)
    print_json(json_for_main, '1.json')
    logger.info('Конец для "Главная"')

    time.sleep(60)

    # Строка для фронтенда 'События'
    logger.info('Для "События" поехали')
    json_for_events = working_with_transactions_events(data_time, 'w')
    print_json(json_for_events, '2.json')
    logger.info('Конец для "События"')


def print_json(data, file):
    logger.info('Начал выводить инфу в JSON-файл, для контроля, пока бэкэндер спит')
    path_file = os.path.dirname(os.path.dirname(__file__)) + "\\data\\"
    with open(path_file + file, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info('Закончил выводить инфу в JSON-файл, для контроля, пока бэкэндер спит')


if __name__ == '__main__':
    main('2018-05-28 12:49:53')
