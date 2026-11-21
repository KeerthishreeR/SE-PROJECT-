"""Lab 7 - fuzz tests for processor.py using Hypothesis.

Contract being tested: for ANY input (random text or None) each function
must either return a sensible value or reject the input with a ValueError.
Any other exception (AttributeError, KeyError, ZeroDivisionError,
OverflowError, ...) is a crash and makes the test fail, which is how the
fuzzer exposes the bugs.

Run from this folder:

    pytest -v test_processor.py
"""

import math
import string

from hypothesis import example, given, strategies as st

from processor import (
    compute_passenger_density,
    lookup_concession_discount,
    parse_transit_corridor,
)

CATEGORIES = ["STANDARD", "STUDENT", "SENIOR", "MILITARY", "CHILD"]


# ---------- fuzzing with arbitrary text / None ----------

@given(st.text() | st.none())
@example(None)
@example("")
@example("A-B-3")
@example("A-B-" + "9" * 400)   # huge zone count -> float overflow
@example("--3")                # empty origin and destination
@example("A-B-1_0")            # underscore accepted by int()
@example("A-B--3")             # negative zones
def test_parse_transit_corridor_no_crash(s):
    try:
        result = parse_transit_corridor(s)
    except ValueError:
        return  # rejecting a bad corridor code with ValueError is correct
    # If it was accepted, the output must have the documented shape.
    assert isinstance(result, str)
    assert result.startswith("Route ")
    assert "Zones, Fare $" in result


@given(st.text() | st.none())
@example(None)
@example("")
@example("VIP")                # unknown category
@example("student")
@example(" Senior ")
def test_lookup_concession_discount_safe(s):
    try:
        discount = lookup_concession_discount(s)
    except ValueError:
        return  # unknown category must be reported as ValueError
    assert 0.0 <= discount <= 1.0


@given(st.text() | st.none())
@example(None)
@example("")
@example("1/0")                # division by zero
@example("1/0.0")
@example("nan/1")              # not a real number
@example("1e999/1")            # infinity
@example("-1/4")               # negative passengers
@example("1/-4")               # negative distance
@example("50/10.0")
def test_compute_passenger_density_safe(s):
    try:
        density = compute_passenger_density(s)
    except ValueError:
        return  # malformed or impossible ratio -> ValueError
    assert math.isfinite(density)
    assert density >= 0


# ---------- fuzzing with well-formed input: results must be correct ----------

LETTERS = st.text(alphabet=string.ascii_letters, min_size=1, max_size=5)


@given(LETTERS, LETTERS, st.integers(min_value=1, max_value=99))
def test_parse_valid_corridor_gives_correct_fare(orig, dest, zones):
    fare = 2.50 + zones * 0.75
    expected = f"Route {orig.upper()}->{dest.upper()}: {zones} Zones, Fare ${fare:.2f}"
    assert parse_transit_corridor(f"{orig}-{dest}-{zones}") == expected


@given(st.sampled_from(CATEGORIES), st.sampled_from(["lower", "upper", "pad"]))
def test_lookup_ignores_case_and_padding(category, style):
    variant = {
        "lower": category.lower(),
        "upper": category.upper(),
        "pad": f"  {category.title()}  ",
    }[style]
    assert lookup_concession_discount(variant) == lookup_concession_discount(category)


@given(st.integers(min_value=0, max_value=10**6),
       st.integers(min_value=1, max_value=10**4))
def test_density_valid_ratio_matches_division(passengers, km):
    assert compute_passenger_density(f"{passengers}/{km}") == round(passengers / km, 2)
