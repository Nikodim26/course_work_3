from datetime import datetime


def top_transaction_record(categories, financial_transactions):
    """Формирует список транзакций"""

    top_transactions = []
    for categori in categories.keys():
        categori_df = financial_transactions.loc[
            (financial_transactions["Категория"] == categori)]

        amount_max = categori_df['Сумма операции'].min()
        top_transactions_df = categori_df.loc[categori_df['Сумма операции'] == amount_max]
        date = str(top_transactions_df.iloc[0, 0])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")

        top_transactions.append(
            {
                "date": date,
                "amount": abs(round(float(amount_max), 2)),
                "category": categori,
                "description": str(top_transactions_df.iloc[0, 6])
            }
        )

    return top_transactions
def recording_card_numbers(card_numbers,types_of_currencies,financial_transactions):
    """Формирует список карт"""

    cards = []
    for card_number in card_numbers:
        for currency in types_of_currencies:
            transaction = financial_transactions.loc[
                (financial_transactions['Номер карты'] == card_number) & (
                        financial_transactions["Валюта операции"] == currency)]

            amount_of_expenses = abs(transaction['Сумма операции'].sum())

            cards.append(
                {
                    "last_digits": card_number[1:],
                    "total_spent": round(float(amount_of_expenses), 2),
                    "cashback": round(float(amount_of_expenses / 100), 2)
                }
            )
    return