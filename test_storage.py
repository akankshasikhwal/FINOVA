# tests/test_storage.py
# Unit tests for save_data and load_data in storage.py.

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from models import BudgetManager
from storage import load_data, save_data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_populated_manager() -> BudgetManager:
    m = BudgetManager()
    m.set_budget(4000.0)
    m.add_expense(150.0, "Food", "Canteen lunch", "2025-07-01")
    m.add_expense(300.0, "Shopping", "Notebook", "2025-07-02")
    return m


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_save_and_load_roundtrip(tmp_path: pytest.TempPathFactory) -> None:
    """Save a manager and load it back — the data should be identical."""
    filepath = str(tmp_path / "test_data.json")
    original = make_populated_manager()

    save_data(original, filepath)
    loaded = load_data(filepath)

    assert loaded.monthly_budget == original.monthly_budget
    assert len(loaded.expenses) == len(original.expenses)

    for orig_exp, loaded_exp in zip(original.expenses, loaded.expenses):
        assert loaded_exp.amount == orig_exp.amount
        assert loaded_exp.category == orig_exp.category
        assert loaded_exp.description == orig_exp.description
        assert loaded_exp.date == orig_exp.date


def test_load_missing_file_returns_empty_manager(tmp_path: pytest.TempPathFactory) -> None:
    """Loading from a non-existent file should return a fresh empty manager."""
    filepath = str(tmp_path / "does_not_exist.json")
    manager = load_data(filepath)

    assert manager.monthly_budget == 0.0
    assert manager.expenses == []


def test_load_corrupt_json_returns_empty_manager(tmp_path: pytest.TempPathFactory) -> None:
    """Loading a file with corrupt JSON should return a fresh empty manager."""
    filepath = str(tmp_path / "corrupt.json")
    with open(filepath, "w") as f:
        f.write("this is not valid json {{{{")

    manager = load_data(filepath)
    assert manager.monthly_budget == 0.0
    assert manager.expenses == []
