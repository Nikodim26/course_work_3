from reading_the_database import working_with_transactions_period


def working_with_transactions_events(request_time: str, period="m"):
    """Функция делает выборки и распечатку транзакций по заданному периоду относительно заданной даты"""

    # Чтение данных и их фильтрация
    df = working_with_transactions_period(request_time, period)

    total_amount_expenses = abs(df.query('`Сумма операции` < 0')['Сумма операции'].sum())  # общие затраты
    total_amount_receipts = df.query('`Сумма операции` > 0')['Сумма операции'].sum()  # общие постуаления

    # затраты по категориям
    category_dictionary = df[df["Сумма операции"] < 0].groupby("Категория")["Сумма операции"].sum()
    category_dictionary = sorted(category_dictionary.items(), key=lambda item: item[1])
    # Траты по 7 категориям
    main = []
    top_expenses = 0
    for i in range(7 if len(category_dictionary) >= 7 else len(category_dictionary)):
        main.append(
            {
                "category": category_dictionary[i][0],
                "amount": round(abs(category_dictionary[i][1]), 2)
            }
        )
        top_expenses += abs(category_dictionary[i][1])

    # Остальные траты
    main.append(
        {
            "category": "Остальное",
            "amount": round(total_amount_expenses - top_expenses, 2)
        }
    )
    category_dictionary = dict(category_dictionary)

    # Траты наличными и переводами
    transfers_and_cash = [
        {
            "category": "Наличные",
            "amount": round(abs(category_dictionary.get("Наличные", 0)), 2)
        },
        {
            "category": "Переводы",
            "amount": round(abs(category_dictionary.get("Переводы", 0)), 2)
        }
    ]
    transfers_and_cash = sorted(transfers_and_cash, key=lambda x: x["amount"], reverse=True)

    # Формирование JSON
    json_str = {
        "expenses": {
            "total_amount": round(total_amount_expenses, 2),
            "main": main,
            'transfers_and_cash': transfers_and_cash
        }
    }

    return json_str
