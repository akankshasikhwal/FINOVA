# SmartSpend – Personal Budget Planner

SmartSpend is a beginner-friendly personal budget planner built with Python and Streamlit. It lets you set a monthly budget, record daily expenses across common categories, and instantly see how much you have left. The app also provides simple, actionable financial-literacy insights — such as your highest spending category and personalised saving tips — so you can build better money habits over time.

This project was built for the **SkillUp Hackathon** in collaboration with **IBM SkillsBuild**, addressing the "AI for Financial Literacy (Student-friendly + real-world)" problem statement.

---

## Features

- Set a monthly budget
- Add expenses with category, description, and date
- View all recorded expenses in a table
- See total spending and remaining budget at a glance
- Get financial insights: highest spending category, budget usage %, and saving suggestions
- Data is saved to a local JSON file and persists across restarts

## Project Structure

```
smartspend/
├── app.py          # Streamlit UI (entry point)
├── models.py       # Expense dataclass + BudgetManager class
├── storage.py      # JSON load/save helpers
├── insights.py     # Financial literacy insight functions
├── constants.py    # Categories, file path, threshold constants
├── exceptions.py   # Custom ValidationError
├── tests/          # Pytest unit tests
├── requirements.txt
└── README.md
```

## Setup & Run

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application** (from inside the `smartspend/` folder)
   ```bash
   streamlit run app.py
   ```

3. **Run the tests** (from inside the `smartspend/` folder)
   ```bash
   pytest
   ```

## Technology

- Python 3.10+
- Streamlit
- JSON (data persistence)
- Pytest (unit tests)
- Type hints throughout
