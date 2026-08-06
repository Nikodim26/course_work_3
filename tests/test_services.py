from services import (determination_of_cashback_categories,
                      receiving_cashback_data)


def test_determination_of_cashback_categories() -> None:
    assert (
        determination_of_cashback_categories(receiving_cashback_data(), "2020", "11")
        == '{\n    "Аптеки": 260,\n    "Транспорт": 15\n}'
    )
    assert determination_of_cashback_categories([], "2020", "11") == "{}"
