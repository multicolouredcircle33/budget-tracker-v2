import math
import csv
import os
from datetime import date, datetime

expenses = []


def console_printer():
    print('--- Personal Budget Tracker ---')
    print('1. Add Expense')
    print('2. View Summary')
    print('3. View Highest-Spending Category')
    print('4. Monthly Summary')
    print('5. Exit')


def load_expenses():
    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "budget_tracker.csv"
    )

    if not os.path.exists(filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "category", "amount"])
        return

    skipped_rows = 0

    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if not row or all(not field.strip() for field in row):
                continue

            try:
                if len(row) != 3:
                    raise ValueError

                expense_date, category, amount_text = row

                parsed_date = datetime.strptime(
                    expense_date, "%Y-%m-%d"
                ).date()

                if parsed_date.isoformat() != expense_date:
                    raise ValueError

                category = clean_category(category)

                cleaned = amount_text.replace(",", "").replace(" ", "")
                amount = float(cleaned)

                if amount <= 0 or not math.isfinite(amount):
                    raise ValueError

                expenses.append((expense_date, category, amount))

            except ValueError:
                skipped_rows += 1

    if skipped_rows:
        row_word = "row" if skipped_rows == 1 else "rows"
        print(
            f"Warning: skipped {skipped_rows} invalid {row_word} "
            "in budget_tracker.csv."
        )


def save_expense(expense_date, category, amount):
    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "budget_tracker.csv"
    )

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "rb+") as file:
            file.seek(-1, os.SEEK_END)

            if file.read(1) not in (b"\n", b"\r"):
                file.write(b"\n")

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([expense_date, category, amount])

def clean_category(text):
    category = " ".join(text.split()).title()

    if not category.replace(" ", "").isalpha():
        raise ValueError

    return category

def record_expense():
    while True:
        try:
            expense_category = clean_category(input(
                'Enter the expense category (e.g. groceries, rent): '
            ))

            break

        except ValueError:
            print('Invalid input! Use only letters and spaces.')

    while True:
        try:
            cleaned = input(
                'Enter the expense amount: '
            ).replace(",", "").replace(" ", "")

            expense_amount = float(cleaned)

            if expense_amount <= 0:
                raise ValueError

            if not math.isfinite(expense_amount):
                raise ValueError

            break

        except ValueError:
            print(
                'Invalid input! Enter a positive amount, '
                'e.g. 50,000 or 12.50.'
            )

    expense_date = date.today().isoformat()

    save_expense(expense_date, expense_category, expense_amount)
    expenses.append((expense_date, expense_category, expense_amount))

    print(f'Expense of ₦{expense_amount:,.2f} added to {expense_category}')
    print('  ')


def category_totals(expenses):
    totals = {}

    for _, category, amount in expenses:
        totals[category] = totals.get(category, 0) + amount

    return totals


def view_summary():
    print('--- Budget Summary ---')

    if not expenses:
        print('No expenses have been recorded.')
        print('  ')
        return

    total_expenses = sum(amount for _, _, amount in expenses)

    print(f'Total Expense: ₦{total_expenses:,.2f}')

    totals = category_totals(expenses)

    for key, value in totals.items():
        print(f'You have spent ₦{value:,.2f} on {key}.')

    print('  ')


def biggest_expense():
    totals = category_totals(expenses)

    if not totals:
        print('No expenses have been recorded.')
        print('  ')
        return

    biggest = max(totals, key=lambda category: totals[category])

    print(
        f'Your highest-spending category is {biggest}: '
        f'₦{totals[biggest]:,.2f}'
    )
    print('  ')

def month_total(records, month):
    return sum(
        amount
        for expense_date, category, amount in records
        if expense_date.startswith(month)
    )

def monthly_summary():
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    while True:
        month_input = input('Enter month (YYYY-MM): ')

        if not (
            len(month_input) == 7
            and month_input[:4].isdigit()
            and month_input[4] == "-"
            and month_input[5:].isdigit()
        ):
            print(
                'Invalid month. Use the format YYYY-MM, '
                'for example 2026-03.'
            )
            continue

        month_number = int(month_input[5:])

        if month_number < 1 or month_number > 12:
            print('Invalid month. Use a month from 1 to 12.')
            continue

        break

    year = month_input[:4]

    total = month_total(expenses, month_input)

    if total == 0:
        print('No expenses have been recorded in this month.')
    else:
        print(
            f'You have spent a total of ₦{total:,.2f} '
            f'in {months[month_number - 1]} {year}.'
        )

    print('  ')


def program_logic():
    while True:
        console_printer()

        while True:
            try:
                operation = int(input('Enter your choice (1-5): '))
                break

            except ValueError:
                print('Invalid input!')

        if operation == 1:
            record_expense()

        elif operation == 2:
            view_summary()

        elif operation == 3:
            biggest_expense()

        elif operation == 4:
            monthly_summary()

        elif operation == 5:
            print('You have successfully exited the program.')
            break

        else:
            print('Please choose a number from 1 to 5.')


if __name__ == "__main__":
    load_expenses()
    program_logic()
