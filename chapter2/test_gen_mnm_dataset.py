import subprocess
import sys
import os
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_PATH = os.path.join(REPO_ROOT, "chapter2", "gen_mnm_dataset.py")

def run_gen_mnm_dataset(*args, cwd=None):
    cmd = [sys.executable, SCRIPT_PATH] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)

def test_gen_mnm_dataset_valid_input(tmp_path):
    res = run_gen_mnm_dataset("10", cwd=tmp_path)
    assert res.returncode == 0
    assert "Wrote 10 lines in mnm_dataset.csv file" in res.stdout
    assert (tmp_path / "mnm_dataset.csv").exists()

def test_gen_mnm_dataset_invalid_string():
    res = run_gen_mnm_dataset("abc")
    assert res.returncode == 255 or res.returncode == -1 or res.returncode == 255 % 256
    assert "Error: Invalid argument for entries: 'abc'. Must be a positive integer." in res.stderr

def test_gen_mnm_dataset_negative_number():
    res = run_gen_mnm_dataset("-5")
    assert res.returncode == 255 or res.returncode == -1 or res.returncode == 255 % 256
    assert "Error: Invalid argument for entries: '-5'. Must be a positive integer." in res.stderr

def test_gen_mnm_dataset_zero():
    res = run_gen_mnm_dataset("0")
    assert res.returncode == 255 or res.returncode == -1 or res.returncode == 255 % 256
    assert "Error: Invalid argument for entries: '0'. Must be a positive integer." in res.stderr

def test_gen_mnm_dataset_missing_args():
    res = run_gen_mnm_dataset()
    assert res.returncode == 255 or res.returncode == -1 or res.returncode == 255 % 256
    assert "Usage: gen_mnm_dataset entries" in res.stderr
