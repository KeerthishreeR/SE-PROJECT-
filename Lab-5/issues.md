# Issues found in `parking_system.py`

Line numbers refer to the **original** file (first commit of this folder).
Rows are ordered by severity, highest first. Rows 1-3 are real bugs that
none of the three tools can flag; I found them by running the program and
reading the output carefully.

**How these were checked.** Flake8 was run on the original file (16 findings:
E302, E305, E501, E722) and on the final file (0 findings). The Pylint and
Bandit codes in the table (W0102, W0702, W0603, W1514, R1732, C0103, C0114,
C0116, B110, B311) were matched to the code by reading it. Compare them with
`reports/before/` and `reports/after/` (made by `make_reports.sh`) and
correct any row that does not match.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Expired permit is not flagged | Bug (High) | 25-30, 60 | `setExpiry` stores `"01/01/2020"` but `is_expired` parses `%Y-%m-%d`. The `ValueError` is swallowed by a bare `except` that returns `False`, so an expired permit counts as valid and `scan_zone` does not flag it. | `set_expiry` validates the date format and rejects bad input. `is_expired` catches only `KeyError`/`ValueError` and treats an unreadable date as expired (fail safe). The demo now uses `2020-01-01`. |
| 2 | No input validation when issuing permits | Bug (High) | 9-17, 57-59 | Zone `"Z"`, an empty plate and a `None` plate are all accepted. The `None` plate is saved as the JSON key `"null"`, and every run adds another duplicate `"null"` key to `permits.json`, which corrupts the database. | `register_permit` returns `None` unless the plate is a non-blank string and the zone is in `ZONES`. |
| 3 | Pressing Enter to "skip" revokes a permit | Bug (Medium) | 63-64 | Skipping passes `""` to `revoke_permit`, which deletes the permit registered under the empty plate. It silently removes a record instead of doing nothing. | Strip the input and only call `revoke_permit` when a plate was actually entered. Empty plates can no longer be registered either (row 2). |
| 4 | Bare `except:` hides every error | Code smell / Bug (High) | 16, 22, 29, 43 | Pylint W0702 and Flake8 E722. It catches everything, including `KeyboardInterrupt`, and hides real failures. In `load_permit_database` a corrupt file silently becomes an empty database, which the next save overwrites. | Catch only the specific exceptions expected: `FileNotFoundError`, `ValueError`, `KeyError`. A corrupt database now prints a warning. |
| 5 | `try` / `except` / `pass` | Security (Low) | 20-23 | Bandit B110. `revoke_permit` ignores any error, so the caller cannot tell whether a revoke worked. | Use `permits.pop(plate, None)` and return `True` or `False` for whether a permit was removed. |
| 6 | Predictable permit numbers from `random` | Security (Low) | 2, 11 | Bandit B311. `random` is not cryptographically secure, so permit numbers can be predicted and forged. | Use `secrets.randbelow()` to generate the number. |
| 7 | Mutable default argument | Bug (Medium) | 9, 14 | Pylint W0102. `zone_records=[]` is created once and shared by every call, so records leak between unrelated calls. | Default to `None` and create a new list inside the function. |
| 8 | File opened without `with`, no encoding | Code smell (Medium) | 42, 47-49 | Pylint R1732 and W1514. `json.load(open(file))` never closes the file, and `save_permit_database` leaks the handle if `json.dump` raises. | Use `with open(file, encoding="utf-8") as handle:` in both functions. |
| 9 | `global` statement | Code smell (Low) | 40-41 | Pylint W0603. Rebinding the module-level dict makes state hard to follow. | Keep one `PERMITS` dict and mutate it with `clear()` and `update()`. |
| 10 | Non-snake_case function name, no validation | Style / Bug (Low) | 51-52 | Pylint C0103 for `setExpiry`. It also raises `KeyError` for an unknown plate. | Rename to `set_expiry` and return `False` for an unknown plate or a bad date. |
| 11 | Missing docstrings | Style (Low) | 1, 9, 19, 25, 32, 39, 46, 51, 54 | Pylint C0114 and C0116 on the module and every function. | Add a module docstring and a short docstring on each function. |
| 12 | `main()` runs on import | Code smell (Low) | 68 | Importing the module executes the demo and writes `permits.json`. | Guard with `if __name__ == "__main__":`. |
| 13 | Formatting: blank lines and line length | Style (Low) | 9-54, 68; 13, 27, 62 | Flake8 E302 and E305 (two blank lines around definitions) and E501 (lines over 79 characters). | Add the blank lines and wrap long lines. |
