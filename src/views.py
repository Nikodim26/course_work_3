from datetime import datetime, timedelta
import pandas as pd

from reading_the_database import about_financial_transactions_xlsx


def aaaaa(request_time):
    # request_time_end = datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S").date()
    # request_time_start = request_time_end - timedelta(days=request_time_end.day - 1)
    request_time_end = request_time[:10]
    request_time_start = request_time[:8] + '01'

    print(request_time_start, request_time_end)

    financial_transactions = about_financial_transactions_xlsx('operations.xlsx').iloc[:, 1:6]

    financial_transactions['Дата платежа'] = pd.to_datetime(financial_transactions['Дата платежа'])

    financial_transactions = financial_transactions.loc[
        (financial_transactions['Дата платежа'].between(request_time_start, request_time_end)) &
    #     (financial_transactions['Дата платежа'] <= pd.to_datetime(request_time_end)) &
    #     (financial_transactions['Дата платежа'] >= pd.to_datetime(request_time_start)) &
        (financial_transactions['Номер карты'].notnull()) &
        (financial_transactions['Статус'].isin(['OK']))]

    # card_numbers = sorted(set(i['Номер карты'] for i in financial_transactions))
    #
    # for card_number in card_numbers:
    #     currencies=set(i["Валюта платежа"] for i in financial_transactions if )

    # amount_of_expenses = [i["Сумма платежа"] for i in financial_transactions if
    #                       i["Номер карты"] == card_number and i["Сумма платежа"] < 0]
    #
    # json_str = f"""
    # Номер карты: {card_number}
    # Общие расходы: {abs(sum(amount_of_expenses))}
    # Kешбэк: {int(sum(amount_of_expenses) / 100) * -1}
    # """

    # break

    return financial_transactions


print((aaaaa('2019-05-20 12:49:53')))
# .to_dict("records")
