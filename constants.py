# constants.py
# Central place for all fixed values used across the application.

# Expense categories available for selection
CATEGORIES: list[str] = ["Food", "Travel", "Shopping", "Education", "Other"]

# Path to the JSON file used for data persistence
DATA_FILE: str = "data.json"

# Percentage threshold at which the app warns the user (0–100)
BUDGET_WARNING_THRESHOLD: float = 80.0
