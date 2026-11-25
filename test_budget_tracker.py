import budget_tracker, pytest

RECORDS = [
    ("2026-10-01", "Food", 1500.0),
    ("2026-10-02", "Rent", 50000.0),
    ("2026-10-03", "Food", 2000.0),
]


def test_starts_with_no_expenses():
    assert budget_tracker.expenses == []


def test_empty_list_gives_empty_dict():
    assert budget_tracker.category_totals([]) == {}


def test_same_category_total_are_added():
    assert budget_tracker.category_totals(RECORDS) == {"Food": 3500.0, "Rent": 50000.0}


def test_diff_categories_stay_separate():
    result = budget_tracker.category_totals(RECORDS)
    assert result["Rent"] == 50000.0


def test_categories_appear_in_same_order_as_list():
    result = budget_tracker.category_totals(RECORDS)
    assert list(result) == ["Food", "Rent"]


def test_input_list_is_not_modified():
    before = list(RECORDS)
    budget_tracker.category_totals(RECORDS)
    assert RECORDS == before

    
def test_digits_are_rejected():
    with pytest.raises(ValueError):
        budget_tracker.clean_category("food2")


def test_spaces_at_both_ends_are_removed():
    assert budget_tracker.clean_category("  food ") == "Food"


def test_each_word_starts_with_a_capital():
    assert budget_tracker.clean_category("food court") == "Food Court"


def test_extra_spaces_between_words_become_one():
    assert budget_tracker.clean_category("food   court") == "Food Court"


def test_empty_text_is_rejected():
    with pytest.raises(ValueError):
        budget_tracker.clean_category("")


def test_only_spaces_is_rejected():
    with pytest.raises(ValueError):
        budget_tracker.clean_category("   ")

MONTH_RECORDS = [
    ("2026-03-05", "Rent", 150000.0),
    ("2026-03-20", "Food", 50000.0),
    ("2026-10-21", "Food", 20000.0),
    ("2025-03-15", "Rent", 1000.0),
]


def test_month_total_counts_only_that_month():
    assert budget_tracker.month_total(MONTH_RECORDS, "2026-03") == 200000.0


def test_month_total_is_zero_when_month_has_no_expenses():
    assert budget_tracker.month_total(MONTH_RECORDS, "2026-11") == 0


def test_month_total_does_not_mix_up_years():
    assert budget_tracker.month_total(MONTH_RECORDS, "2025-03") == 1000.0


COUNT_RECORDS = [
    ("2026-10-05", "Food", 1500.0),
    ("2026-10-10", "Rent", 50000.0),
    ("2026-10-21", "Food", 2000.0),
]


def test_count_above_counts_records_over_limit():
    assert budget_tracker.count_above(COUNT_RECORDS, 1800) == 2


def test_count_above_only_one_over_limit():
    assert budget_tracker.count_above(COUNT_RECORDS, 10000) == 1


def test_count_above_equal_to_limit_not_counted():
    assert budget_tracker.count_above(COUNT_RECORDS, 50000) == 0


def test_count_above_zero_limit_counts_all():
    assert budget_tracker.count_above(COUNT_RECORDS, 0) == 3


def test_count_above_empty_list_gives_zero():
    assert budget_tracker.count_above([], 1000) == 0

def test_count_above_works_with_decimal_limit():
    assert budget_tracker.count_above(COUNT_RECORDS, 1999.99) == 2


def test_count_above_does_not_change_records():
    before = list(COUNT_RECORDS)
    budget_tracker.count_above(COUNT_RECORDS, 1800)
    assert COUNT_RECORDS == before

def test_range_total_some_records_in_range():
    assert budget_tracker.range_total(COUNT_RECORDS, "2026-10-01", "2026-10-15") == 51500.0


def test_range_total_single_day_included():
    assert budget_tracker.range_total(COUNT_RECORDS, "2026-10-05", "2026-10-05") == 1500.0


def test_range_total_both_ends_included():
    assert budget_tracker.range_total(COUNT_RECORDS, "2026-10-10", "2026-10-21") == 52000.0


def test_range_total_no_records_in_range():
    assert budget_tracker.range_total(COUNT_RECORDS, "2026-11-01", "2026-11-30") == 0


def test_range_total_empty_list_gives_zero():
    assert budget_tracker.range_total([], "2026-01-01", "2026-12-31") == 0

def test_range_total_start_after_end_gives_zero():
    assert budget_tracker.range_total(COUNT_RECORDS, "2026-10-21", "2026-10-01") == 0


def test_range_total_does_not_change_records():
    before = list(COUNT_RECORDS)
    budget_tracker.range_total(COUNT_RECORDS, "2026-10-01", "2026-10-31")
    assert COUNT_RECORDS == before


def test_parse_amount_removes_commas():
    assert budget_tracker.parse_amount("50,000") == 50000.0


def test_parse_amount_strips_outer_spaces():
    assert budget_tracker.parse_amount(" 12.50 ") == 12.5


def test_parse_amount_removes_inner_spaces():
    assert budget_tracker.parse_amount("1 500") == 1500.0


@pytest.mark.parametrize("text", ["0", "-5", "abc", "inf", "nan", ""])
def test_parse_amount_rejects_bad_input(text):
    with pytest.raises(ValueError):
        budget_tracker.parse_amount(text)


def test_parse_month_accepts_valid_month():
    assert budget_tracker.parse_month("2026-03") == "2026-03"


@pytest.mark.parametrize("text", ["2026-3", "March", ""])
def test_parse_month_rejects_wrong_format(text):
    with pytest.raises(ValueError, match="format YYYY-MM"):
        budget_tracker.parse_month(text)


@pytest.mark.parametrize("text", ["2026-13", "2026-00"])
def test_parse_month_rejects_month_out_of_range(text):
    with pytest.raises(ValueError, match="1 to 12"):
        budget_tracker.parse_month(text)


CSV_HEADER_AND_TWO_ROWS = (
    "date,category,amount\n"
    "2026-10-05,food,1500.0\n"
    "2026-10-10,Rent,50000\n"
)

TWO_RECORDS = [
    ("2026-10-05", "Food", 1500.0),
    ("2026-10-10", "Rent", 50000.0),
]


def test_read_expenses_reads_valid_rows(tmp_path):
    data = tmp_path / "data.csv"
    data.write_text(CSV_HEADER_AND_TWO_ROWS)
    assert budget_tracker.read_expenses(data) == (TWO_RECORDS, 0)


def test_read_expenses_counts_invalid_row(tmp_path):
    data = tmp_path / "data.csv"
    data.write_text(CSV_HEADER_AND_TWO_ROWS + "05/10/2026,Food,100\n")
    assert budget_tracker.read_expenses(data) == (TWO_RECORDS, 1)


def test_read_expenses_ignores_blank_rows(tmp_path):
    data = tmp_path / "data.csv"
    data.write_text(CSV_HEADER_AND_TWO_ROWS + "\n")
    assert budget_tracker.read_expenses(data) == (TWO_RECORDS, 0)


def test_read_expenses_missing_file_gives_empty_and_creates_nothing(tmp_path):
    missing = tmp_path / "missing.csv"
    assert budget_tracker.read_expenses(missing) == ([], 0)
    assert not missing.exists()


def test_read_expenses_does_not_touch_global_list(tmp_path):
    data = tmp_path / "data.csv"
    data.write_text(CSV_HEADER_AND_TWO_ROWS)
    before = list(budget_tracker.expenses)
    budget_tracker.read_expenses(data)
    assert budget_tracker.expenses == before