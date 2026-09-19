# tests/test_models.py
# Unit tests for BudgetManager and Expense in models.py.

import sys
import os

# Make sure the smartspend package root is on the path when running pytest
# from inside the smartspend/ directory or the workspace root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from exceptions import ValidationError
from models import BudgetManager, Expense


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_manager(budget: float = 5000.0) -> BudgetManager:
    """Return a BudgetManager with a preset budget."""
    m = BudgetManager()
    m.set_budget(budget)
    return m


# ---------------------------------------------------------------------------
# set_budget
# ---------------------------------------------------------------------------

def test_set_budget_valid() -> None:
    m = BudgetManager()
    m.set_budget(3000.0)
    assert m.monthly_budget == 3000.0


def test_set_budget_zero_raises() -> None:
    m = BudgetManager()
    with pytest.raises(ValidationError):
        m.set_budget(0.0)


def test_set_budget_negative_raises() -> None:
    m = BudgetManager()
    with pytest.raises(ValidationError):
        m.set_budget(-500.0)


# ---------------------------------------------------------------------------
# add_expense — happy path
# ---------------------------------------------------------------------------

def test_add_expense_valid() -> None:
    m = make_manager()
    expense = m.add_expense(200.0, "Food", "Lunch", "2025-07-01")
    assert isinstance(expense, Expense)
    assert expense.amount == 200.0
    assert expense.category == "Food"
    assert expense.description == "Lunch"
    assert expense.date == "2025-07-01"
    assert len(m.expenses) == 1


# ---------------------------------------------------------------------------
# add_expense — validation failures
# ---------------------------------------------------------------------------

def test_add_expense_negative_amount_raises() -> None:
    m = make_manager()
    with pytest.raises(ValidationError):
        m.add_expense(-50.0, "Food", "Lunch", "2025-07-01")


def test_add_expense_zero_amount_raises() -> None:
    m = make_manager()
    with pytest.raises(ValidationError):
        m.add_expense(0.0, "Food", "Lunch", "2025-07-01")


def test_add_expense_empty_description_raises() -> None:
    m = make_manager()
    with pytest.raises(ValidationError):
        m.add_expense(100.0, "Food", "", "2025-07-01")


def test_add_expense_whitespace_description_raises() -> None:
    m = make_manager()
    with pytest.raises(ValidationError):
        m.add_expense(100.0, "Food", "   ", "2025-07-01")


def test_add_expense_invalid_category_raises() -> None:
    m = make_manager()
    with pytest.raises(ValidationError):
        m.add_expense(100.0, "Gambling", "Casino night", "2025-07-01")


def test_add_expense_invalid_date_raises() -> None:
    m = make_manager()
    with pytest.raises(ValidationError):
        m.add_expense(100.0, "Food", "Lunch", "not-a-date")


# ---------------------------------------------------------------------------
# total_spent
# ---------------------------------------------------------------------------

def test_total_spent_no_expenses() -> None:
    m = make_manager()
    assert m.total_spent() == 0.0


def test_total_spent_with_expenses() -> None:
    m = make_manager()
    m.add_expense(100.0, "Food", "Breakfast", "2025-07-01")
    m.add_expense(250.0, "Travel", "Bus pass", "2025-07-02")
    assert m.total_spent() == 350.0


# ---------------------------------------------------------------------------
# remaining_budget
# ---------------------------------------------------------------------------

def test_remaining_budget() -> None:
    m = make_manager(budget=1000.0)
    m.add_expense(300.0, "Shopping", "T-shirt", "2025-07-03")
    assert m.remaining_budget() == 700.0


def test_remaining_budget_negative_when_overspent() -> None:
    m = make_manager(budget=100.0)
    m.add_expense(150.0, "Food", "Dinner", "2025-07-04")
    assert m.remaining_budget() == -50.0


# ---------------------------------------------------------------------------
# spending_by_category
# ---------------------------------------------------------------------------

def test_spending_by_category() -> None:
    m = make_manager()
    m.add_expense(200.0, "Food", "Lunch", "2025-07-01")
    m.add_expense(100.0, "Food", "Coffee", "2025-07-02")
    m.add_expense(500.0, "Travel", "Flight", "2025-07-03")
    by_cat = m.spending_by_category()
    assert by_cat["Food"] == 300.0
    assert by_cat["Travel"] == 500.0
    assert "Shopping" not in by_cat
