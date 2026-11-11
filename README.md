# Budget Tracker v2

A personal budget tracker that runs in the terminal. Record your expenses, see where your money goes, and get the total for any month. Every expense is saved to a CSV file, so your data is still there the next time you open it.

## What it does

1. **Add Expense:** enter a category and an amount. Today's date is added automatically.
2. **View Summary:** your total spending, and the total for each category.
3. **View Highest-Spending Category:** the category you spent the most on.
4. **Monthly Summary:** the total for any month you choose, entered as YYYY-MM.
5. **Exit**

Money is always shown like this: ₦1,500.00

## Requirements

Python 3 (tested with Python 3.14 on Windows). The tracker itself needs no extra packages. pytest is needed only to run the tests.

## How to run it

```
git clone https://github.com/multicolouredcircle33/budget-tracker-v2.git
cd budget-tracker-v2
python budget_tracker.py
```

On Windows, if `python` is not recognised, use `py budget_tracker.py`.

Example:

```
--- Personal Budget Tracker ---
1. Add Expense
2. View Summary
3. View Highest-Spending Category
4. Monthly Summary
5. Exit
Enter your choice (1-5): 1
Enter the expense category (e.g. groceries, rent): food
Enter the expense amount: 20000
Expense of ₦20,000.00 added to Food
```

## How to run the tests

```
pip install -r requirements-dev.txt
pytest
```

Every test should pass.

## Your data

The first time you run the tracker, it creates `budget_tracker.csv` in the same folder. Each expense is one line: `date,category,amount`.

1. The file is listed in `.gitignore`, so your spending is never uploaded to GitHub.
2. If you edit it by hand, use a text editor such as VS Code. Spreadsheet programs can change the dates, and rows with changed dates are skipped.
3. Invalid rows are skipped, with a warning that says how many.

## Project files

```
budget_tracker.py        the tracker
test_budget_tracker.py   the tests (pytest)
requirements-dev.txt     what you need to run the tests
.gitignore               keeps personal data and generated files out of Git
```

## Not included (yet)

1. Editing or deleting an expense after it is added
2. Summaries for a range of dates
3. Tests for the amount check