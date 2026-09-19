# tests/test_insights.py
# Unit tests for the pure insight functions in insights.py.

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from insights import (
    budget_used_percent,
    highest_spending_category,
    is_near_budget,
    saving_suggestion,
)


# ---------------------------------------------------------------------------
# highest_spending_category
# ---------------------------------------------------------------------------

def test_highest_spending_category() -> None:
    spending = {"Food": 300.0, "Travel": 500.0, "Shopping": 200.0}
    assert highest_spending_category(spending) == "Travel"


def test_highest_spending_category_empty() -> None:
    assert highest_spending_category({}) is None


# ---------------------------------------------------------------------------
# budget_used_percent
# ---------------------------------------------------------------------------

def test_budget_used_percent() -> None:
    result = budget_used_percent(400.0, 1000.0)
    assert result == 40.0


def test_budget_used_percent_zero_budget() -> None:
    # Must return 0.0 and not raise ZeroDivisionError
    result = budget_used_percent(500.0, 0.0)
    assert result == 0.0


def test_budget_used_percent_full_spend() -> None:
    result = budget_used_percent(1000.0, 1000.0)
    assert result == 100.0


def test_budget_used_percent_overspend() -> None:
    result = budget_used_percent(1200.0, 1000.0)
    assert result == 120.0


# ---------------------------------------------------------------------------
# is_near_budget
# ---------------------------------------------------------------------------

def test_is_near_budget_true_at_threshold() -> None:
    assert is_near_budget(80.0, 80.0) is True


def test_is_near_budget_true_above_threshold() -> None:
    assert is_near_budget(95.0, 80.0) is True


def test_is_near_budget_false() -> None:
    assert is_near_budget(50.0, 80.0) is False


# ---------------------------------------------------------------------------
# saving_suggestion
# ---------------------------------------------------------------------------

def test_saving_suggestion_over_budget() -> None:
    result = saving_suggestion("Food", 105.0)
    assert "exceeded" in result.lower()


def test_saving_suggestion_near_budget() -> None:
    result = saving_suggestion("Shopping", 85.0)
    assert "close" in result.lower() or "cut back" in result.lower()


def test_saving_suggestion_food() -> None:
    result = saving_suggestion("Food", 50.0)
    assert result != ""
    assert "food" in result.lower() or "meal" in result.lower()


def test_saving_suggestion_shopping() -> None:
    result = saving_suggestion("Shopping", 50.0)
    assert result != ""
    assert "purchase" in result.lower() or "impulse" in result.lower()


def test_saving_suggestion_travel() -> None:
    result = saving_suggestion("Travel", 50.0)
    assert result != ""
    assert "travel" in result.lower() or "carpool" in result.lower()


def test_saving_suggestion_education() -> None:
    result = saving_suggestion("Education", 50.0)
    assert result != ""
    assert "resource" in result.lower() or "free" in result.lower()


def test_saving_suggestion_none_category() -> None:
    result = saving_suggestion(None, 30.0)
    assert result != ""


def test_saving_suggestion_not_empty() -> None:
    """saving_suggestion always returns a non-empty string."""
    result = saving_suggestion("Other", 60.0)
    assert isinstance(result, str)
    assert len(result) > 0
