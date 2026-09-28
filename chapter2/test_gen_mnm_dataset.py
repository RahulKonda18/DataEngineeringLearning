import pytest
from unittest.mock import patch
from chapter2.gen_mnm_dataset import get_random_choice


def test_get_random_choice_returns_item_from_list():
    sample_list = ["CA", "WA", "TX"]
    result = get_random_choice(sample_list)
    assert result in sample_list


def test_get_random_choice_calls_random_choice():
    sample_list = ["Brown", "Blue", "Orange"]
    with patch("random.choice", return_value="Blue") as mock_choice:
        result = get_random_choice(sample_list)
        assert result == "Blue"
        mock_choice.assert_called_once_with(sample_list)


def test_get_random_choice_empty_list_raises_index_error():
    with pytest.raises(IndexError):
        get_random_choice([])
