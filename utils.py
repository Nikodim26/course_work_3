from datetime import datetime


def top_transaction_record(card_numbers, types_of_currencies, categories, financial_transactions):
    """Формирует список топовых транзакций в рублях"""

    top_transactions = []
    for card_number in card_numbers:
        for currency in types_of_currencies:
            for categori in categories:
                df = financial_transactions.loc[
                    (financial_transactions["Категория"] == categori) &
                    (financial_transactions['Номер карты'] == card_number) &
                    (financial_transactions["Валюта операции"] == currency)
                    ]
                if not df.empty:
                    amount_max = df['Сумма операции'].min()

                    top_transactions_df = df.loc[df['Сумма операции'] == amount_max]
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

    top_transactions=sorted(top_transactions,key=lambda x:x["amount"],reverse=True)[:5]

    return top_transactions


def recording_card_numbers(card_numbers, types_of_currencies, financial_transactions):
    """Формирует список карт"""

    cards = []
    for card_number in card_numbers:
        for currency in types_of_currencies:
            df = financial_transactions.loc[
                (financial_transactions['Номер карты'] == card_number) &
                (financial_transactions["Валюта операции"] == currency)
                ]
            if not df.empty:
                amount_of_expenses = abs(df['Сумма операции'].sum())
                cards.append(
                    {
                        "last_digits": card_number[1:],
                        "total_spent": round(float(amount_of_expenses), 2),
                        "cashback": round(float(amount_of_expenses / 100), 2),
                    }
                )
    return cards
