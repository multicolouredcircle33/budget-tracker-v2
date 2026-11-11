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