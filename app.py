# app.py
# Streamlit UI for SmartSpend – Personal Budget Planner.
# This file only handles the user interface.
# All business logic lives in models.py, storage.py, and insights.py.

import datetime

import streamlit as st

from constants import BUDGET_WARNING_THRESHOLD, CATEGORIES, DATA_FILE
from exceptions import ValidationError
from insights import (
    budget_used_percent,
    highest_spending_category,
    is_near_budget,
    saving_suggestion,
)
from storage import load_data, save_data

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SmartSpend – Personal Budget Planner",
    page_icon="💰",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Load data once per session (or when the page refreshes)
# ---------------------------------------------------------------------------
# We store the BudgetManager in Streamlit's session_state so changes made
# during the session are kept in memory between widget interactions.
if "manager" not in st.session_state:
    st.session_state.manager = load_data(DATA_FILE)

manager = st.session_state.manager

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("💰 SmartSpend")
st.caption("Personal Budget Planner · SkillUp Hackathon × IBM SkillsBuild")
st.divider()

# ---------------------------------------------------------------------------
# Section 1 — Set Monthly Budget
# ---------------------------------------------------------------------------
st.subheader("📋 Set Monthly Budget")

budget_input = st.number_input(
    label="Enter your monthly budget (₹)",
    min_value=0.01,
    step=100.0,
    value=float(manager.monthly_budget) if manager.monthly_budget > 0 else 1000.0,
    format="%.2f",
    key="budget_input",
)

if st.button("Set Budget", type="primary"):
    try:
        manager.set_budget(budget_input)
        save_data(manager, DATA_FILE)
        st.success(f"Monthly budget set to ₹{manager.monthly_budget:,.2f}")
    except ValidationError as e:
        st.error(str(e))

if manager.monthly_budget > 0:
    st.info(f"Current monthly budget: **₹{manager.monthly_budget:,.2f}**")
else:
    st.warning("No budget set yet. Please enter a budget above.")

st.divider()

# ---------------------------------------------------------------------------
# Section 2 — Add Expense
# ---------------------------------------------------------------------------
st.subheader("➕ Add Expense")

col1, col2 = st.columns(2)

with col1:
    expense_amount = st.number_input(
        label="Amount (₹)",
        min_value=0.01,
        step=10.0,
        format="%.2f",
        key="expense_amount",
    )
    expense_category = st.selectbox(
        label="Category",
        options=CATEGORIES,
        key="expense_category",
    )

with col2:
    expense_description = st.text_input(
        label="Description",
        placeholder="e.g. Lunch at canteen",
        key="expense_description",
    )
    expense_date = st.date_input(
        label="Date",
        value=datetime.date.today(),
        key="expense_date",
    )

if st.button("Add Expense", type="primary"):
    try:
        expense = manager.add_expense(
            amount=expense_amount,
            category=expense_category,
            description=expense_description,
            date=str(expense_date),
        )
        save_data(manager, DATA_FILE)
        st.success(
            f"Expense added: ₹{expense.amount:,.2f} for {expense.category} "
            f"on {expense.date}"
        )
    except ValidationError as e:
        st.error(str(e))

st.divider()

# ---------------------------------------------------------------------------
# Section 3 — Summary
# ---------------------------------------------------------------------------
st.subheader("📊 Summary")

total = manager.total_spent()
remaining = manager.remaining_budget()

sum_col1, sum_col2, sum_col3 = st.columns(3)

sum_col1.metric(label="Monthly Budget", value=f"₹{manager.monthly_budget:,.2f}")
sum_col2.metric(label="Total Spent", value=f"₹{total:,.2f}")
sum_col3.metric(
    label="Remaining",
    value=f"₹{remaining:,.2f}",
    delta=f"₹{remaining:,.2f}",
    delta_color="normal" if remaining >= 0 else "inverse",
)

if remaining < 0:
    st.error(
        f"⚠️ You have overspent your budget by ₹{abs(remaining):,.2f}! "
        "Please review your expenses."
    )

st.divider()

# ---------------------------------------------------------------------------
# Section 4 — Expense Table
# ---------------------------------------------------------------------------
st.subheader("📝 All Expenses")

if manager.expenses:
    # Build a plain list of dicts for the table — no pandas dependency needed.
    rows = [
        {
            "Date": e.date,
            "Category": e.category,
            "Description": e.description,
            "Amount (₹)": f"{e.amount:,.2f}",
        }
        for e in sorted(manager.expenses, key=lambda x: x.date, reverse=True)
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)

    # Category-wise spending table
    st.subheader("🗂️ Category-wise Spending")
    cat_spending = manager.spending_by_category()
    cat_rows = [
        {"Category": cat, "Total Spent (₹)": f"{amt:,.2f}"}
        for cat, amt in sorted(cat_spending.items(), key=lambda x: x[1], reverse=True)
    ]
    st.dataframe(cat_rows, use_container_width=True, hide_index=True)
else:
    st.info("No expenses recorded yet. Add your first expense above!")

st.divider()

# ---------------------------------------------------------------------------
# Section 5 — Financial Insights
# ---------------------------------------------------------------------------
st.subheader("💡 Financial Insights")

if not manager.expenses:
    st.info(
        "Add some expenses to see your personalised financial insights here."
    )
else:
    cat_spending = manager.spending_by_category()
    top_cat = highest_spending_category(cat_spending)
    pct_used = budget_used_percent(total, manager.monthly_budget)
    near = is_near_budget(pct_used, BUDGET_WARNING_THRESHOLD)
    suggestion = saving_suggestion(top_cat, pct_used)

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        st.metric(
            label="Budget Used",
            value=f"{pct_used:.1f}%",
            delta=f"{pct_used:.1f}% of ₹{manager.monthly_budget:,.2f}",
            delta_color="off",
        )

    with insight_col2:
        if top_cat:
            st.metric(
                label="Highest Spending Category",
                value=top_cat,
                delta=f"₹{cat_spending[top_cat]:,.2f} spent",
                delta_color="off",
            )

    if near:
        st.warning(
            f"🚨 You have used **{pct_used:.1f}%** of your budget. "
            "Consider slowing down your spending!"
        )

    st.info(f"💬 Saving tip: {suggestion}")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "SmartSpend · Built for the SkillUp Hackathon × IBM SkillsBuild · "
    "Data stored locally in data.json"
)
