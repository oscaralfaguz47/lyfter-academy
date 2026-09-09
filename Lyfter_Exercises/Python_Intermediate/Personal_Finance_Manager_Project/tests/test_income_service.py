
from unittest.mock import patch
from services.income_service import create_income


def test_create_expense_saves_new_expense():
    with patch("services.income_service.get_data_from_csv", return_value=[]):
        with patch("services.income_service.save_data_to_csv") as mock_save:
            result = create_income("Other Sales", "100000", "o30c2fd9-411f-4a63-8dab-3a659f0ee895")

            mock_save.assert_called_once()
            assert result.transaction_title == "Other Sales" and result.amount == "100000" and result.id_category == "o30c2fd9-411f-4a63-8dab-3a659f0ee895"