import os
import pytest
from chapter2.mnmcount import validate_file_path


def test_validate_file_path_valid(tmp_path):
    test_file = tmp_path / "dataset.csv"
    test_file.write_text("State,Color,Count\nCA,Blue,10\n")

    validated = validate_file_path(str(test_file))
    assert validated == os.path.abspath(str(test_file))


def test_validate_file_path_non_existent():
    with pytest.raises(FileNotFoundError, match="Specified file does not exist"):
        validate_file_path("non_existent_file.csv")


def test_validate_file_path_empty():
    with pytest.raises(ValueError, match="File path cannot be empty"):
        validate_file_path("")


def test_validate_file_path_directory(tmp_path):
    with pytest.raises(ValueError, match="Specified path is not a file"):
        validate_file_path(str(tmp_path))
