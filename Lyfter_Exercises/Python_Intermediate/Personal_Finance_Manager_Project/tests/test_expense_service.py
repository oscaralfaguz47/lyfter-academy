
from unittest.mock import patch
from services.expense_service import create_expense


def test_create_expense_saves_new_expense():
    with patch("services.expense_service.get_data_from_csv", return_value=[]):
        with patch("services.expense_service.save_data_to_csv") as mock_save:
            result = create_expense("Gasoline", "5000", "e30c7fd9-311f-4a63-8dab-3af59f0ee895")

            mock_save.assert_called_once()
            assert result.transaction_title == "Gasoline" and result.amount == "5000" and result.id_category == "e30c7fd9-311f-4a63-8dab-3af59f0ee895"