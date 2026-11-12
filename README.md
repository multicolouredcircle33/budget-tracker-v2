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

## How AI was used

I built this project while studying how useful AI is in software engineering, so this section records exactly what AI did, what I did, and how each part was checked.

| Part | Who did it | How it was checked |
|---|---|---|
| Version 1 of the tracker | Me | An AI code review. I checked each point it raised, and 3 of 3 were correct |
| Specification for v2 | Me, in three drafts. Claude then asked me 53 questions to find gaps and wrote the final spec from my answers | I read the final spec against my answers |
| v2 code | ChatGPT, built in three steps from my spec | I ran worked examples after each step |
| `category_totals` and `month_total` | ChatGPT, from a short description. It never saw my tests | My tests, written first. 8 of 8 passed on the first try |
| Tests | Me | I watched each test fail before the code existed, then pass after |
| README, sample data and the GitHub test workflow | Drafted by Claude from the actual code | I ran the commands and checked the results |

### What went wrong

1. **A gap in the spec.** It never said what to do when the CSV file does not end with a new line. ChatGPT followed the spec exactly, so a new expense got glued onto the last row. I found it by testing with a file saved from a spreadsheet, and fixed it.
2. **An unrequested change.** When I asked ChatGPT to reprint the whole file, it quietly rewrote a function I had not asked it to touch. Now I ask for one function at a time and compare.
3. **A category bug.** Extra spaces between words (for example `Fast   Food`) were not removed. A test caught it, I worked out the cause, and fixed it.

### What I learned

AI writes correct code quickly when the description is exact, but it also builds the gaps in that description exactly. Writing the tests myself is how I know the code does what I meant.