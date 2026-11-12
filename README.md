# Budget Tracker v2

A personal budget tracker that runs in the terminal. Expenses are saved to a CSV file, so your data is still there the next time you open it.

## What it does

1. **Add Expense:** enter a category and an amount. Today's date is added automatically.
2. **View Summary:** your total spending and the total for each category.
3. **View Highest-Spending Category:** the category you spent the most on.
4. **Monthly Summary:** the total for a month you choose, entered as YYYY-MM.
5. **Exit**

Money is shown in Naira, for example ₦1,500.00.

## Requirements

Python 3 (tested with Python 3.14 on Windows). The tracker needs no extra packages. pytest is only needed to run the tests.

## How to run it

```
git clone https://github.com/multicolouredcircle33/budget-tracker-v2.git
cd budget-tracker-v2
python budget_tracker.py
```

On Windows, if `python` is not recognised, use `py budget_tracker.py`.

Example session (adding a ₦20,000 food expense, then viewing the summary):

```
--- Personal Budget Tracker ---
1. Add Expense
2. View Summary
3. View Highest-Spending Category
4. Monthly Summary
5. Exit
Enter your choice (1-5): 1
Enter the expense category (e.g. groceries, rent): food
Enter the expense amount: 20,000
Expense of ₦20,000.00 added to Food

Enter your choice (1-5): 2
--- Budget Summary ---
Total Expense: ₦20,000.00
You have spent ₦20,000.00 on Food.
```

## Try it with sample data

`sample_budget_tracker.csv` holds six made-up expenses so you can see the summaries without typing anything in.

1. Copy it to the file name the program reads.
   Windows (PowerShell): `Copy-Item sample_budget_tracker.csv budget_tracker.csv`
   Mac or Linux: `cp sample_budget_tracker.csv budget_tracker.csv`
2. Run `python budget_tracker.py` and choose option 2. The total should be ₦60,000.00, with Rent (₦50,000.00) as the biggest category.
3. Choose option 4 and enter `2026-10`. You should see ₦56,500.00.

Copying replaces any `budget_tracker.csv` you already have, so do this before you record your own expenses.

## How to run the tests

```
pip install -r requirements-dev.txt
pytest
```

Every test should pass.

## Your data

The first time you run the tracker, it creates `budget_tracker.csv` in the same folder. Each expense is one line in the form `date,category,amount`.

This file is listed in `.gitignore`, so your spending is never uploaded to GitHub.

If you edit the file by hand, use a text editor, not a spreadsheet program. Spreadsheets can change the date format, and rows with a changed date are skipped. When rows are skipped, the tracker prints a warning with the number of rows.

## Project files

| File | What it is |
|---|---|
| `budget_tracker.py` | The tracker |
| `test_budget_tracker.py` | pytest tests |
| `sample_budget_tracker.csv` | Made-up expenses for trying the tracker |
| `requirements-dev.txt` | What to install to run the tests |
| `.gitignore` | Keeps personal data and practice files off GitHub |

## Not included (yet)

1. Editing or deleting an expense
2. Summaries over a date range
3. Tests for the amount check