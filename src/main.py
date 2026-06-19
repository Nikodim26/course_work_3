import json
import os
import time

from views import working_with_transactions
from views_events import working_with_transactions_events


def main(data_time: str) -> None:
    """Функция выдает JSON строки для фронтенда 'Главная' и 'События'"""

    # Строка для фронтенда 'Главная'
    json_for_main = working_with_transactions(data_time)
    print_json(json_for_main, '1.json')

    time.sleep(15)

    # Строка для фронтенда 'События'
    json_for_events = working_with_transactions_events(data_time, 'w')
    print_json(json_for_events, '2.json')


def print_json(data, file):
    path_file = os.path.dirname(os.path.dirname(__file__)) + "\\data\\"
    with open(path_file + file, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main('2018-05-28 12:49:53')
