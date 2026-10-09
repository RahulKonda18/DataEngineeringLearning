import csv
from pathlib import Path
import runpy
import sys
import pytest
from chapter2.gen_mnm_dataset import get_random_choice

def test_get_random_choice():
    sample_list = ["CA", "WA", "TX", "NV"]
    for _ in range(20):
        choice = get_random_choice(sample_list)
        assert choice in sample_list

def test_gen_mnm_dataset_generation(tmp_path, monkeypatch, capsys):
    script_path = Path(__file__).resolve().parent.parent / "gen_mnm_dataset.py"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["gen_mnm_dataset.py", "10"])

    runpy.run_path(str(script_path), run_name="__main__")

    captured = capsys.readouterr()
    assert "Wrote 10 lines in mnm_dataset.csv file" in captured.out

    csv_file = tmp_path / "mnm_dataset.csv"
    assert csv_file.exists()

    expected_states = {"CA", "WA", "TX", "NV", "CO", "OR", "AZ", "WY", "NM", "UT"}
    expected_colors = {"Brown", "Blue", "Orange", "Yellow", "Green", "Red"}

    with open(csv_file, mode="r", newline="") as f:
        reader = list(csv.reader(f))

        # Header + 9 data rows = 10 lines
        assert len(reader) == 10
        assert reader[0] == ["State", "Color", "Count"]

        for row in reader[1:]:
            assert len(row) == 3
            state, color, count_str = row
            assert state in expected_states
            assert color in expected_colors
            count = int(count_str)
            assert 10 <= count <= 100

@pytest.mark.parametrize(
    "invalid_argv",
    [
        ["gen_mnm_dataset.py"],
        ["gen_mnm_dataset.py", "10", "extra_arg"],
    ],
)
def test_gen_mnm_dataset_invalid_args(invalid_argv, tmp_path, monkeypatch, capsys):
    script_path = Path(__file__).resolve().parent.parent / "gen_mnm_dataset.py"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", invalid_argv)

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(str(script_path), run_name="__main__")

    assert exc_info.value.code == -1
    captured = capsys.readouterr()
    assert "Usage: gen_mnm_dataset entries" in captured.err
