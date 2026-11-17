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