from views import working_with_transactions


def test_working_with_transactions() -> None:
    json_dict = working_with_transactions('2018-05-28 12:49:53')
    headlines = [i for i in json_dict.keys()]
    assert "greeting" in headlines
    assert "cards" in headlines
    assert "top_transactions" in headlines
    assert "currency_rates" in headlines
    assert "stock_prices" in headlines

