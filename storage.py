# storage.py
# Handles saving and loading BudgetManager data to/from a JSON file.
# This module is the only place in the application that touches the file system.

import json
import os

from models import BudgetManager, Expense


def save_data(manager: BudgetManager, filepath: str) -> None:
    """Serialize a BudgetManager to a JSON file.

    Args:
        manager:  The BudgetManager instance to save.
        filepath: Path to the JSON file to write.
    """
    data = {
        "monthly_budget": manager.monthly_budget,
        "expenses": [
            {
                "amount": e.amount,
                "category": e.category,
                "description": e.description,
                "date": e.date,
            }
            for e in manager.expenses
        ],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_data(filepath: str) -> BudgetManager:
    """Deserialize a BudgetManager from a JSON file.

    If the file does not exist or contains invalid JSON, a fresh empty
    BudgetManager is returned so the application never crashes on startup.

    Args:
        filepath: Path to the JSON file to read.

    Returns:
        A BudgetManager populated with the saved data, or a new empty one.
    """
    manager = BudgetManager()

    if not os.path.exists(filepath):
        return manager

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        manager.monthly_budget = float(data.get("monthly_budget", 0.0))

        for item in data.get("expenses", []):
            expense = Expense(
                amount=float(item["amount"]),
                category=item["category"],
                description=item["description"],
                date=item["date"],
            )
            manager.expenses.append(expense)

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        # If the file is corrupt or has unexpected data, start fresh.
        return BudgetManager()

    return manager
