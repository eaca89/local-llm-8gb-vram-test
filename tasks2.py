"""Implement every function so it does exactly what its docstring says. Standard library only."""


def merge_intervals(intervals):
    """intervals: list of [start, end] integer pairs, unsorted, may overlap.
    Return the merged list sorted by start. Pairs that share an end point merge ([1, 3] + [3, 5] -> [1, 5]),
    but pairs that only sit next to each other do not ([1, 3] + [4, 5] stay separate). [] -> []."""


def parse_csv_line(line):
    """Parse one CSV line into a list of strings. Fields are separated by commas. A field may be wrapped in
    double quotes; inside a quoted field a comma is literal and a doubled quote "" means one quote character.
    Unquoted fields are returned exactly as written, spaces included. 'a,"b,c",d' -> ['a', 'b,c', 'd'].
    An empty line returns ['']."""


def business_days_between(start, end, holidays):
    """start and end are "YYYY-MM-DD" strings, holidays a list of "YYYY-MM-DD" strings.
    Count the weekdays (Mon-Fri) after start up to and including end that are not holidays.
    If end is before start, return the negative of the count from end to start. Same day -> 0."""


def round_money(x):
    """Round a float to 2 decimals, half away from zero, the way a person would on paper:
    2.675 -> 2.68, 1.005 -> 1.01, -1.005 -> -1.01, 2.5 -> 2.5. Return a float."""


def to_roman(n):
    """Integer 1..3999 -> Roman numeral string (4 -> 'IV', 1994 -> 'MCMXCIV').
    Anything else, including bools and floats, raises ValueError."""


def chunk_words(text, size, overlap):
    """Split text on whitespace into chunks of at most `size` words, joined by single spaces.
    Each chunk starts `size - overlap` words after the previous one; stop once a chunk reaches the last word.
    overlap must satisfy 0 <= overlap < size, otherwise raise ValueError. Empty or blank text -> []."""
