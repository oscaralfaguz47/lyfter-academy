
import pytest
from unittest.mock import patch
from models.category import Category

from services.category_service import create_category 

def test_create_category_saves_new_category():
    with patch("services.category_service.get_data_from_csv", return_value=[]):
        with patch("services.category_service.save_data_to_csv") as mock_save:
            result = create_category("Travel")

            mock_save.assert_called_once()
            assert result.category_name == "Travel"

def test_create_category_does_not_allow_create_category_with_duplicated_category_name():
    existing = [Category("Travel")]
    with patch("services.category_service.get_data_from_csv", return_value=existing):
        with patch("services.category_service.save_data_to_csv") as mock_save:
            with pytest.raises(ValueError, match=f"The category 'Travel' already exists"):
                create_category("Travel")
            mock_save.assert_not_called()
