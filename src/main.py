import json
import os

from views import working_with_transactions
from views_events import working_with_transactions_events


def main(data_time: str) -> list:
    """Функция выдает JSON строки для фронтенда 'Главная' и 'События'"""

    path_file = os.path.dirname(os.path.dirname(__file__)) + "\\data\\"

    # # Строка для фронтенда 'Главная'
    # json_for_main = working_with_transactions(data_time)
    #
    # with open(path_file + '1.json', 'w', encoding="utf-8") as f:
    #     json.dump(json_for_main, f, indent=4, ensure_ascii=False)

    # Строка для фронтенда 'События'
    json_for_events = working_with_transactions_events(data_time, 'm')

    with open(path_file + '2.json', 'w', encoding="utf-8") as f:
        json.dump(json_for_events, f, indent=4, ensure_ascii=False)



if __name__ == '__main__':

    main('2018-05-28 12:49:53')

