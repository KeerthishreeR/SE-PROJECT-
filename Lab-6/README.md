# Lab 6: Code and Branch Coverage (bus transit fare)

| File | Purpose |
|------|---------|
| `bus_transit_fare.py` | Module under test (unchanged) |
| `test_bus_transit.py` | Starter test (unchanged) |
| `CodeCoverageTest_bus_transit_application.py` | Tests for over 90% **line** coverage |
| `BranchCoverageTest_bus_transit_application.py` | Tests for over 90% **branch** coverage |
| `screenshots/` | Terminal screenshots of the coverage reports |

## Run (from this folder, virtual environment active)

```bash
pip install coverage pytest

# Line coverage
coverage run -m pytest CodeCoverageTest_bus_transit_application.py
coverage report -m

# Branch coverage
coverage run --branch -m pytest BranchCoverageTest_bus_transit_application.py
coverage report -m
```

The test files are named so that pytest does not pick them up on its own,
so always pass the file name as shown.
