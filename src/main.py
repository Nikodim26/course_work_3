import json
import os

from reading_the_database import working_with_transactions_period
from views import working_with_transactions


def main():
    return working_with_transactions('2018-05-28 12:49:53','m')


if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + '1.json'
    data_json = main()
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)
