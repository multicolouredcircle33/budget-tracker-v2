# SPEC: Budget Tracker, web edition (capstone)

## Purpose
The same budget tracker as a web page. Same data file and same rules as the
terminal version, which must keep working exactly as before.

## Files
- budget_tracker.py: 3 new functions (Parts 1, 1b, 2); record_expense,
  monthly_summary and load_expenses changed to use them; nothing else changes
- app.py: NEW, the Streamlit page (Part 3)
- test_budget_tracker.py: new tests for Parts 1, 1b and 2
- requirements.txt: NEW, streamlit==1.67.0
- requirements-dev.txt: add the line -r requirements.txt (so CI installs Streamlit)
- README.md: new section on how to run the web version

## Part 1: parse_amount(text)
- Purpose: turn what the user typed into an amount, with the terminal's rules
- Returns: a float
- Rules:
  1. remove commas and spaces, then convert with float()
  2. raise ValueError if it cannot convert, if amount <= 0, or if it is not finite (inf, nan)
  3. no printing, no input()
- Examples: "50,000" → 50000.0 · " 12.50 " → 12.5 · "1 500" → 1500.0 ·
  "0", "-5", "abc", "inf", "" → ValueError
- Also: record_expense uses it; its messages and behaviour stay the same

## Part 1b: parse_month(text)
- Purpose: check a month typed as YYYY-MM, with the terminal's rules
- Returns: the same text, e.g. "2026-03"
- Rules:
  1. exactly 7 characters: 4 digits, "-", 2 digits, otherwise
     ValueError("Invalid month. Use the format YYYY-MM, for example 2026-03.")
  2. the month must be 01 to 12, otherwise
     ValueError("Invalid month. Use a month from 1 to 12.")
  3. no printing, no input()
- Examples: "2026-03" → "2026-03" · "2026-3", "March", "" → format error ·
  "2026-13", "2026-00" → 1 to 12 error
- Also: monthly_summary uses it: it prints the error's message and asks again;
  its messages and behaviour stay the same

## Part 2: read_expenses(filename)
- Purpose: read the CSV and return the valid records WITHOUT using the global
  `expenses` list and WITHOUT printing, so the web page can call it on every re-run
- Returns: (records, skipped)
  - records: list of (date, category, amount) tuples, in file order
  - skipped: number of invalid rows
- Rules:
  1. skip the header line
  2. blank rows are ignored and NOT counted as skipped
  3. a row is invalid (skipped + 1) if: not exactly 3 fields, date is not a real
     YYYY-MM-DD date, category fails clean_category, or amount fails parse_amount
  4. categories are stored cleaned (clean_category)
  5. file missing → ([], 0), and the file is NOT created
- Examples:
  - header + "2026-10-05,food,1500.0" + "2026-10-10,Rent,50000"
    → ([("2026-10-05", "Food", 1500.0), ("2026-10-10", "Rent", 50000.0)], 0)
  - the same + "05/10/2026,Food,100" → same records, skipped 1
  - the same + a blank line → skipped still 0
  - missing file → ([], 0)
- Also: load_expenses keeps its job (creates the file if missing, prints the
  warning, fills `expenses`) but uses read_expenses inside

## Part 3: app.py, the page from top to bottom
1. Title "Budget Tracker"
2. records, skipped = read_expenses(budget_tracker.csv next to budget_tracker.py);
   skipped > 0 → warning "Skipped N invalid row(s) in budget_tracker.csv."
3. Add expense: text box Category, text box Amount, button Add
   - invalid category → error "Invalid input! Use only letters and spaces."
   - invalid amount → error "Invalid input! Enter a positive amount, e.g. 50,000 or 12.50."
   - valid → save_expense(today, category, amount), append the record to `records`
     so the sections below include it, and show "Expense of ₦X added to Category"
4. Summary: no records → "No expenses have been recorded."; otherwise the total,
   a table of category totals (category_totals), one bar chart of category totals,
   and the highest-spending category with its amount
5. Monthly total: text box "Month (YYYY-MM)"
   - empty → show nothing
   - invalid → error with parse_month's message
   - valid → month_total → "You have spent a total of ₦X in October 2026."
     or, if the total is 0,
"No expenses have been recorded in this month."
6. Date range: From and To date pickers (default: 1st of this month, today)
   → range_total → "You spent ₦X between A and B."
7. Over an amount: number box (minimum 0, default 10,000)
   → count_above → "N expense(s) cost more than ₦X."

Money is always shown as ₦{x:,.2f}.

## Out of scope
Editing or deleting expenses, logins, putting the app online, more than one chart.

## Done when
1. pytest: all tests pass (29 + the new ones)
2. python budget_tracker.py behaves exactly as before
3. streamlit run app.py shows all 7 parts; an expense added on the web appears in
   the terminal version too (same CSV)
4. a fresh clone works by following only the README, and CI stays green
