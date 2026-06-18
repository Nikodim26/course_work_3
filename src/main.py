import json
import os

from reading_the_database import working_with_transactions_period
from views import working_with_transactions
from views_events import working_with_transactions_events


def main():
    """Функция выдает JSON строки"""

    main_json=working_with_transactions('2018-05-28 12:49:53','m')
    # json_events=working_with_transactions_events('2018-05-28 12:49:53','m')

    # return json_events
    return main_json#,json_events


if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + '1.json'
    data_json = main()
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)
