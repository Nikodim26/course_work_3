from pathlib import Path

import pandas as pd

from reports import (receiving_a_dataframe_with_transactions,
                     spending_by_category)

data_path = Path(__file__).resolve().parent.parent / "data" / "df.xlsx"


def test_spending_by_category() -> None:
    assert (
        spending_by_category(receiving_a_dataframe_with_transactions(), "Супермаркеты") is None
    )
    assert data_path.exists()
    saved_df = pd.read_excel(data_path)
    expected_df = saved_df.loc[saved_df["Категория"] == "Супермаркеты"]
    pd.testing.assert_frame_equal(saved_df, expected_df)
