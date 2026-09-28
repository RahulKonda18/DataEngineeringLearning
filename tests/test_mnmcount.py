import runpy
import sys
from unittest.mock import MagicMock
import pytest


def test_mnmcount_cli_missing_args(monkeypatch, capsys):
    """Test that mnmcount.py exits with status -1 and prints usage when no filename argument is provided."""
    monkeypatch.setattr(sys, "argv", ["mnmcount.py"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path("chapter2/mnmcount.py", run_name="__main__")

    assert exc_info.value.code == -1
    captured = capsys.readouterr()
    assert "Usage: mnmcount <file>" in captured.err


def test_mnmcount_cli_too_many_args(monkeypatch, capsys):
    """Test that mnmcount.py exits with status -1 and prints usage when too many arguments are provided."""
    monkeypatch.setattr(sys, "argv", ["mnmcount.py", "file1.csv", "file2.csv"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path("chapter2/mnmcount.py", run_name="__main__")

    assert exc_info.value.code == -1
    captured = capsys.readouterr()
    assert "Usage: mnmcount <file>" in captured.err


def test_mnmcount_cli_valid_args(monkeypatch, capsys):
    """Test that mnmcount.py passes CLI check when exactly one filename argument is provided."""
    monkeypatch.setattr(sys, "argv", ["mnmcount.py", "chapter2/mnm_dataset.csv"])

    mock_pyspark_sql = MagicMock()
    mock_spark = MagicMock()
    mock_df = MagicMock()
    mock_pyspark_sql.SparkSession.builder.appName.return_value.getOrCreate.return_value = mock_spark
    mock_spark.read.format.return_value.option.return_value.option.return_value.load.return_value = mock_df
    mock_df.select.return_value.groupBy.return_value.sum.return_value.orderBy.return_value = mock_df
    mock_df.select.return_value.where.return_value.groupBy.return_value.sum.return_value.orderBy.return_value = mock_df
    mock_df.count.return_value = 100

    monkeypatch.setitem(sys.modules, "pyspark.sql", mock_pyspark_sql)

    runpy.run_path("chapter2/mnmcount.py", run_name="__main__")

    captured = capsys.readouterr()
    assert "Usage: mnmcount <file>" not in captured.err
