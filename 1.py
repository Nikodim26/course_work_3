import os

import pandas as pd


def about_financial_transactions_xlsx(file_data: str) -> Any:
    """Принимает на вход путь до XLSX-файла и возвращает список словарей с данными о финансовых транзакциях"""

    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + file_data
    try:
        reader_xlsx = pd.read_excel(path)
        transactions = reader_xlsx.to_dict("records")
        return transactions

    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return []



print(about_financial_transactions_xlsx())