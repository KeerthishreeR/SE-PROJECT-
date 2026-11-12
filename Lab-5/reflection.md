# Reflection

## 1. What did each tool catch, and which was most useful?

Pylint caught the most: the mutable default argument, the bare `except`
clauses, files opened without `with`, the `global` statement, the camelCase
name and the missing docstrings. Bandit reported only two low-severity
items (`random` in a security-sensitive spot and a `try`/`except`/`pass`).
Flake8 reported only formatting: blank lines and line length. Pylint was
the most useful because it pointed at real design problems, while Bandit
was the most focused: few findings, but both were worth fixing.

## 2. What did the tools miss?

The worst bugs were invisible to all three tools. A permit with an expiry
of `01/01/2020` was never flagged as expired, because the date format did
not match and a bare `except` hid the error. Pressing Enter to skip
actually revoked the empty-plate permit, and a `None` plate was saved as
`"null"` and duplicated on every run. I found these only by running the
program and reading its output. The tools check how code is written, not
whether it does what the author intended.

## 3. How did fixing the issues change the code?

The code now rejects bad input (blank plates, unknown zones, malformed
dates) instead of storing it, and it no longer hides errors. It fails
safe: an unreadable expiry counts as expired. State is easier to follow:
one `PERMITS` dict, no `global`, no shared default list, and importing the
module no longer runs the program. Each change was small, but together
they removed the silent failures that made the original hard to trust.

## 4. How would I use static analysis in a real project?

I would run all three tools automatically (a pre-commit hook and CI) so
that problems are caught while the change is still fresh, and I would
fail the build on new Bandit and Pylint errors. I would still keep
tests and code review, because static analysis cannot find logic bugs
like the expiry-date one. I would also treat every warning as a question
rather than an order: some can be false positives or a matter of taste,
and the fix should be chosen on purpose, not just to silence the tool.
