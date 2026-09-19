# models.py
# Core data models and business logic for SmartSpend.
# This module has no Streamlit dependency — it can be imported and tested independently.

import datetime
from dataclasses import dataclass, field

from constants import CATEGORIES
from exceptions import ValidationError


@dataclass
class Expense:
    """Represents a single expense entry.

    Attributes:
        amount:      The expense amount (must be > 0).
        category:    One of the predefined categories (e.g. "Food").
        description: A short description of the expense.
        date:        The date of the expense in ISO format (YYYY-MM-DD).
    """

    amount: float
    category: str
    description: str
    date: str


class BudgetManager:
    """Manages the monthly budget and the list of expenses.

    This is the main business-logic class. The Streamlit UI creates one
    instance of this class (loaded from JSON) and calls its methods.

    Attributes:
        monthly_budget: The user's budget for the current month.
        expenses:       The list of Expense objects recorded so far.
    """

    def __init__(self) -> None:
        self.monthly_budget: float = 0.0
        self.expenses: list[Expense] = []

    # ------------------------------------------------------------------
    # Mutating methods
    # ------------------------------------------------------------------

    def set_budget(self, amount: float) -> None:
        """Set the monthly budget.

        Args:
            amount: The budget value. Must be greater than zero.

        Raises:
            ValidationError: If amount is zero or negative.
        """
        if amount <= 0:
            raise ValidationError("Monthly budget must be greater than zero.")
        self.monthly_budget = amount

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        date: str,
    ) -> Expense:
        """Validate and add a new expense.

        Args:
            amount:      The expense amount (must be > 0).
            category:    Must be one of CATEGORIES.
            description: Must not be empty or whitespace-only.
            date:        Must be a valid date string in YYYY-MM-DD format.

        Returns:
            The newly created Expense object.

        Raises:
            ValidationError: If any field is invalid.
        """
        # Validate amount
        if amount <= 0:
            raise ValidationError("Expense amount must be greater than zero.")

        # Validate category
        if category not in CATEGORIES:
            raise ValidationError(
                f"Category must be one of: {', '.join(CATEGORIES)}."
            )

        # Validate description
        if not description.strip():
            raise ValidationError("Description cannot be empty.")

        # Validate date
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            raise ValidationError(
                "Date must be a valid date in YYYY-MM-DD format."
            )

        expense = Expense(
            amount=amount,
            category=category,
            description=description.strip(),
            date=date,
        )
        self.expenses.append(expense)
        return expense

    # ------------------------------------------------------------------
    # Read-only / calculation methods
    # ------------------------------------------------------------------

    def total_spent(self) -> float:
        """Return the total amount spent across all expenses."""
        return sum(e.amount for e in self.expenses)

    def remaining_budget(self) -> float:
        """Return how much budget is left.

        Can be negative if the user has overspent.
        """
        return self.monthly_budget - self.total_spent()

    def spending_by_category(self) -> dict[str, float]:
        """Return a mapping of category name to total amount spent in that category."""
        totals: dict[str, float] = {}
        for expense in self.expenses:
            totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
        return totals
