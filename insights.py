# insights.py
# Pure functions that derive financial-literacy insights from spending data.
# These functions have no side effects and no Streamlit dependency.


def highest_spending_category(spending: dict[str, float]) -> str | None:
    """Return the category with the highest total spending.

    Args:
        spending: A dict mapping category names to total amounts spent.

    Returns:
        The category name with the highest spend, or None if spending is empty.
    """
    if not spending:
        return None
    return max(spending, key=lambda cat: spending[cat])


def budget_used_percent(total_spent: float, budget: float) -> float:
    """Return what percentage of the budget has been spent.

    Returns 0.0 when the budget is zero to avoid division by zero.

    Args:
        total_spent: Total amount spent so far.
        budget:      The monthly budget.

    Returns:
        A float between 0.0 and (potentially above) 100.0.
    """
    if budget <= 0:
        return 0.0
    return (total_spent / budget) * 100.0


def is_near_budget(percent_used: float, threshold: float) -> bool:
    """Return True if spending has reached or exceeded the threshold percentage.

    Args:
        percent_used: The percentage of budget already spent.
        threshold:    The warning threshold (e.g. 80.0 for 80 %).

    Returns:
        True if percent_used >= threshold.
    """
    return percent_used >= threshold


def saving_suggestion(highest_cat: str | None, percent_used: float) -> str:
    """Return a simple, actionable saving tip based on the user's spending.

    Args:
        highest_cat:  The category with the highest spending, or None.
        percent_used: The percentage of budget already spent.

    Returns:
        A human-readable saving suggestion string.
    """
    if percent_used >= 100:
        return "You have exceeded your budget! Avoid all non-essential spending."

    if percent_used >= 80:
        cat_text = highest_cat if highest_cat else "general"
        return (
            f"You are close to your budget limit. "
            f"Try to cut back on {cat_text} expenses."
        )

    if highest_cat == "Food":
        return "Consider meal prepping to reduce food expenses."

    if highest_cat == "Shopping":
        return (
            "Try a 24-hour rule before making purchases — "
            "it reduces impulse buying."
        )

    if highest_cat == "Travel":
        return "Look for student travel discounts or carpool options."

    if highest_cat == "Education":
        return "Check for free resources like YouTube or free courses online."

    if highest_cat in (None, "Other"):
        return "Track every small expense — they add up quickly!"

    return "Keep tracking your expenses to build better habits."
