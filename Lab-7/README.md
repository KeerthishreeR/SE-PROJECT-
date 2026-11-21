# Lab 7: Fuzz Testing with Hypothesis (bus transit processor)

| File | Purpose |
|------|---------|
| `processor.py` | Module under test (fixed in the last code commit) |
| `test_processor.py` | Hypothesis fuzz tests |
| `screenshots/` | Terminal screenshots (failing run before the fix, passing run after) |

## Run (virtual environment active)

```bash
pip install hypothesis pytest
pytest -v test_processor.py
```

To see the crashes Hypothesis finds, check out the tests-only commit
(`git log --oneline` shows it as "complete Hypothesis fuzz tests"), run
`pytest -v test_processor.py`, then return to `main`.

## Contract the tests enforce

For any input (random text or `None`) each function returns a sensible
value or raises `ValueError`. Any other exception counts as a crash.

## Bugs found and fixed

| # | Function | Input | Original behaviour | Fix |
|---|----------|-------|--------------------|-----|
| 1 | all three | `None` | `AttributeError` (`.strip` / `.split` on None) | Reject non-text with `ValueError` |
| 2 | `lookup_concession_discount` | `"VIP"`, `""` | `KeyError` | Unknown category raises `ValueError` |
| 3 | `compute_passenger_density` | `"1/0"` | `ZeroDivisionError` | Require km greater than zero |
| 4 | `parse_transit_corridor` | `"A-B-" + "9"*400` | `OverflowError` (int too large for float) | Limit zones to 1-99 |
| 5 | `parse_transit_corridor` | `"--3"` | Accepted: `Route ->: 3 Zones` | Origin and destination must not be empty |
| 6 | `parse_transit_corridor` | `"A-B-1_0"` | Accepted as 10 zones | Zones must be plain ASCII digits |
| 7 | `compute_passenger_density` | `"-1/4"`, `"1/-4"` | Negative density returned | Reject negative passengers and non-positive km |
| 8 | `compute_passenger_density` | `"nan/1"`, `"1e999/1"` | Returned `nan` / `inf` | Reject non-finite numbers and results |
| 9 | `main()` | any bad input | Program crashed with a traceback | Catch `ValueError` and print a message |
