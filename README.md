# Budget Tracker v2

[![tests](https://github.com/multicolouredcircle33/budget-tracker-v2/actions/workflows/tests.yml/badge.svg)](https://github.com/multicolouredcircle33/budget-tracker-v2/actions/workflows/tests.yml)

**Demo:** [watch the 3-minute video](https://drive.google.com/file/d/1uTkv5LtoNosHpu_bAF75HCoCqGif-hE2/view?usp=sharing)

A personal budget tracker you can use in the terminal or in your browser. Expenses are saved to a CSV file, so your data is still there the next time you open it. Both versions share the same file and the same rules.

## What it does

1. **Add Expense:** enter a category and an amount. Today's date is added automatically.
2. **View Summary:** your total spending and the total for each category.
3. **View Highest-Spending Category:** the category you spent the most on.
4. **Monthly Summary:** the total for a month you choose, entered as YYYY-MM.
5. **Exit**

The web version also shows a bar chart of your categories, the total between any two dates, and how many expenses cost more than an amount you choose.

Money is shown in Naira, for example ₦1,500.00.

## What you need

1. **Python 3** (tested with Python 3.14 on Windows). If you don't have it, install the free **Python install manager** from the Microsoft Store (or from python.org). Then open a terminal and type `python`. The first time, it downloads Python for you. If it asks to add a folder to your PATH, say yes.
2. **The code.** Click the green **Code** button at the top of this page, then **Download ZIP**, and unzip it. If you use Git, you can run `git clone https://github.com/multicolouredcircle33/budget-tracker-v2.git` instead.

The terminal version needs nothing else. The web version needs Streamlit, which you install with one command below.

## Open a terminal in the project folder

On Windows, open the unzipped folder in File Explorer. Use the folder that contains `README.md` and `app.py`; after unzipping, it may be inside a second folder with the same name. Click the address bar, type `powershell` and press Enter. A terminal opens in that folder.

## How to run it (terminal version)

```
python budget_tracker.py
```

If `python` is not recognised, use `py budget_tracker.py`.

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

## Run the web version

```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The first command downloads Streamlit, which takes about a minute on a new computer. The second opens the page in your browser at `http://localhost:8501`. Add an expense, then look at the summary, bar chart, monthly total, date range and "over an amount" sections. In the Month box, type a month such as `2026-10` and press Enter. To stop the app, press Ctrl+C in the terminal.

## Try it with sample data

`sample_budget_tracker.csv` holds six made-up expenses so you can see the summaries without typing anything in.

1. Copy it to the file name the program reads.
   Windows (PowerShell): `Copy-Item sample_budget_tracker.csv budget_tracker.csv`
   Mac or Linux: `cp sample_budget_tracker.csv budget_tracker.csv`
2. Run `python budget_tracker.py` and choose option 2, or open the web version. The total should be ₦60,000.00, with Rent (₦50,000.00) as the biggest category.
3. In option 4, or the web page's Month box, enter `2026-10`. You should see ₦56,500.00.

Copying replaces any `budget_tracker.csv` you already have, so do this before you record your own expenses.

## How to run the tests

```
python -m pip install -r requirements-dev.txt
python -m pytest
```

Every test should pass.

## Your data

The first time you run the tracker, it creates `budget_tracker.csv` in the same folder. Each expense is one line in the