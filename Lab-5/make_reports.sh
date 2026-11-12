#!/usr/bin/env bash
# Generate the Pylint, Bandit and Flake8 reports.
#
#   ./make_reports.sh before   # analyses the ORIGINAL starter file
#   ./make_reports.sh after    # analyses the CURRENT parking_system.py
#
# Reports are written to reports/before/ or reports/after/.
# Run it with your virtual environment active (pylint, bandit, flake8 installed).

set -u
cd "$(dirname "$0")"

mode="${1:-}"
case "$mode" in
  before | after) ;;
  *) echo "Usage: $0 before|after"; exit 1 ;;
esac

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

if [ "$mode" = "before" ]; then
  # The commit that first added the file is the untouched starter version.
  first="$(git log --diff-filter=A --format=%H -1 -- parking_system.py)"
  git show "$first:./parking_system.py" > "$work/parking_system.py"
else
  cp parking_system.py "$work/parking_system.py"
fi

out="reports/$mode"
mkdir -p "$out"
(
  cd "$work" || exit 1
  python3 -m pylint parking_system.py > "$OLDPWD/$out/pylint_report.txt"
  python3 -m bandit -r parking_system.py > "$OLDPWD/$out/bandit_report.txt" 2>&1
  python3 -m flake8 parking_system.py > "$OLDPWD/$out/flake8_report.txt"
)

echo "== $mode =="
grep -h "rated at" "$out/pylint_report.txt" || echo "Pylint: no score line found"
echo "Bandit issues: $(grep -c '>> Issue' "$out/bandit_report.txt")"
echo "Flake8 problems: $(wc -l < "$out/flake8_report.txt" | tr -d ' ')"
echo "Reports saved in Lab-5/$out/"
