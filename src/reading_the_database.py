import json
import os

import pandas as pd


def about_financial_transactions_xlsx(file_data: str) -> list[dict]:
    """Принимает на вход путь до XLSX-файла и возвращает список словарей с данными о финансовых транзакциях"""

    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + file_data
    try:
        return pd.read_excel(path)
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return []

# transactions=about_financial_transactions_xlsx('operations.xlsx')
# print(json.dumps(transactions[0],ensure_ascii=False,indent=4))