import json
import os

import pandas as pd


def about_financial_transactions_xlsx(file_data: str) -> list[dict]:
    """Принимает на вход путь до XLSX-файла и возвращает список словарей с данными о финансовых транзакциях"""

    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + file_data
    try:
        return pd.read_excel(path).to_dict("records")
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return []


transactions=about_financial_transactions_xlsx('operations.xlsx')
times=[i['Дата операции'] for i in transactions]
print(min(times),max(times))

# for i in transactions:
#
#     print(json.dumps(i,ensure_ascii=False,indent=4))
#     break