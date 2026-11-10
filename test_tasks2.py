import pytest
from tasks2 import merge_intervals, parse_csv_line, business_days_between, round_money, to_roman, chunk_words


def test_mi_basic(): assert merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]
def test_mi_unsorted(): assert merge_intervals([[8, 10], [1, 3], [2, 4]]) == [[1, 4], [8, 10]]
def test_mi_touch(): assert merge_intervals([[1, 3], [3, 5]]) == [[1, 5]]
def test_mi_adjacent(): assert merge_intervals([[1, 3], [4, 5]]) == [[1, 3], [4, 5]]
def test_mi_empty(): assert merge_intervals([]) == []
def test_mi_inside(): assert merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]
def test_csv_plain(): assert parse_csv_line("a,b,c") == ["a", "b", "c"]
def test_csv_quoted(): assert parse_csv_line('a,"b,c",d') == ["a", "b,c", "d"]
def test_csv_dq(): assert parse_csv_line('"say ""hi""",x') == ['say "hi"', "x"]
def test_csv_spaces(): assert parse_csv_line(" a , b") == [" a ", " b"]
def test_csv_emptyfields(): assert parse_csv_line("a,,") == ["a", "", ""]
def test_csv_empty(): assert parse_csv_line("") == [""]
def test_bd_week(): assert business_days_between("2026-11-06", "2026-11-13", []) == 5
def test_bd_same(): assert business_days_between("2026-11-09", "2026-11-09", []) == 0
def test_bd_holiday(): assert business_days_between("2026-11-09", "2026-11-13", ["2026-11-11"]) == 3
def test_bd_reverse(): assert business_days_between("2026-11-13", "2026-11-06", []) == -5
def test_bd_weekend_hol(): assert business_days_between("2026-11-06", "2026-11-09", ["2026-11-08"]) == 1
def test_rm_2675(): assert round_money(2.675) == 2.68
def test_rm_1005(): assert round_money(1.005) == 1.01
def test_rm_neg(): assert round_money(-1.005) == -1.01
def test_rm_plain(): assert round_money(2.5) == 2.5
def test_ro_4(): assert to_roman(4) == "IV"
def test_ro_1994(): assert to_roman(1994) == "MCMXCIV"
def test_ro_3999(): assert to_roman(3999) == "MMMCMXCIX"
def test_ro_zero():
    with pytest.raises(ValueError): to_roman(0)
def test_ro_big():
    with pytest.raises(ValueError): to_roman(4000)
def test_ro_bool():
    with pytest.raises(ValueError): to_roman(True)
def test_ro_float():
    with pytest.raises(ValueError): to_roman(3.0)
def test_cw_basic(): assert chunk_words("a b c d e", 2, 0) == ["a b", "c d", "e"]
def test_cw_overlap(): assert chunk_words("a b c d e", 3, 1) == ["a b c", "c d e"]
def test_cw_spaces(): assert chunk_words("  a   b  ", 5, 0) == ["a b"]
def test_cw_empty(): assert chunk_words("   ", 3, 1) == []
def test_cw_bad():
    with pytest.raises(ValueError): chunk_words("a b", 2, 2)
