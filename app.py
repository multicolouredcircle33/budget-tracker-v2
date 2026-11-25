import os
import csv
from datetime import date

import streamlit as st
import budget_tracker as bt


# Page configuration
st.set_page_config(page_title="Budget Tracker", page_icon="💰", layout="wide")

st.title("Budget Tracker")


# File path
path = os.path.join(
    os.path.dirname(os.path.abspath(bt.__file__)),
    "budget_tracker.csv"
)


# Helper function for formatting money
def format_money(amount):
    return f"₦{amount:,.2f}"


# Load records fresh on every Streamlit rerun
records, skipped = bt.read_expenses(path)

if skipped > 0:
    st.warning(f"Skipped {skipped} invalid row(s) in budget_tracker.csv.")


# --------------------------------------------------
# Add Expense
# --------------------------------------------------

st.header("Add Expense")

with st.form("add_expense_form"):
    category_input = st.text_input("Category")
    amount_input = st.text_input("Amount")
    submitted = st.form_submit_button("Add")

    if submitted:
        try:
            category = bt.clean_category(category_input)
        except ValueError:
            st.error("Invalid input! Use only letters and spaces.")
        else:
            try:
                amount = bt.parse_amount(amount_input)
            except ValueError:
                st.error(
                    "Invalid input! Enter a positive amount, "
                    "e.g. 50,000 or 12.50."
                )
            else:
                # Create the CSV file with its header if it does not exist
                if not os.path.exists(path):
                    with open(path, "w", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(["date", "category", "amount"])

                # Save the expense
                today = date.today().strftime("%Y-%m-%d")
                bt.save_expense(today, category, amount)

                # Include the new expense in the current run
                records.append((today, category, amount))

                st.success(
                    f"Expense of {format_money(amount)} added to {category}"
                )


# --------------------------------------------------
# Summary
# --------------------------------------------------

st.header("Summary")

if not records:
    st.info("No expenses have been recorded.")
else:
    total = sum(record[2] for record in records)
    st.metric("Total Expenses", format_money(total))

    totals = bt.category_totals(records)

    # Category totals table
    st.subheader("Category Totals")

    category_data = [
        {
            "Category": category,
            "Amount": format_money(amount)
        }
        for category, amount in totals.items()
    ]

    st.table(category_data)

    # One bar chart of category totals
    st.subheader("Spending by Category")
    st.bar_chart(totals)

    # Highest-spending category
    highest_category = max(totals, key=totals.get)
    highest_amount = totals[highest_category]

    st.write(
        f"Highest-spending category: "
        f"{highest_category} ({format_money(highest_amount)})"
    )


# --------------------------------------------------
# Monthly Total
# --------------------------------------------------

st.header("Monthly Total")

month_input = st.text_input("Month (YYYY-MM)")

if month_input.strip():
    try:
        month = bt.parse_month(month_input)
    except ValueError as error:
        st.error(str(error))
    else:
        monthly_total = bt.month_total(records, month)

        if monthly_total == 0:
            st.info("No expenses have been recorded in this month.")
        else:
            month_date = date.fromisoformat(month + "-01")
            month_name = month_date.strftime("%B %Y")

            st.write(
                f"You have spent a total of "
                f"{format_money(monthly_total)} in {month_name}."
            )

# --------------------------------------------------
# Date Range
# --------------------------------------------------

st.header("Date Range")

today = date.today()
first_day_of_month = today.replace(day=1)

from_date = st.date_input(
    "From",
    value=first_day_of_month
)

to_date = st.date_input(
    "To",
    value=today
)

if from_date > to_date:
    st.error("The start date cannot be after the end date.")
else:
    start = from_date.strftime("%Y-%m-%d")
    end = to_date.strftime("%Y-%m-%d")

    range_expenses = bt.range_total(records, start, end)

    st.write(
        f"You spent {format_money(range_expenses)} "
        f"between {start} and {end}."
    )


# --------------------------------------------------
# Over an Amount
# --------------------------------------------------

st.header("Over an Amount")

limit = st.number_input(
    "Amount (₦)",
    min_value=0.0,
    value=10000.0,
    step=1000.0
)

count = bt.count_above(records, limit)

expense_word = "expense" if count == 1 else "expenses"

st.write(
    f"{count} {expense_word} cost more than {format_money(limit)}."
)