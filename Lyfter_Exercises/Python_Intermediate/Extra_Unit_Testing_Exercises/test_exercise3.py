
from unittest.mock import mock_open, patch
import pytest


def read_lines(path):
    with open(path, 'r') as f:
        return f.readlines()

#------------ TESTS --------------------->

def test_read_file_content():
    fake_content = "My line one\nMy line two\nMy line three\n"

    with patch("builtins.open", mock_open(read_data=fake_content)):
        result = read_lines("file_path.txt")

    assert result == ["My line one\n", "My line two\n", "My line three\n"]

def test_read_lines_raises_error_when_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        read_lines("non_exist.txt")