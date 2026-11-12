"""Lab 6 - tests written to reach (at least) 90% LINE coverage.

This first pass covers the main paths. The remaining gaps (senior fares, a
blacklisted card on a non-express route, the audit failure) are closed in
BranchCoverageTest_bus_transit_application.py.

Run from the Lab-6 folder:

    coverage run -m pytest CodeCoverageTest_bus_transit_application.py
    coverage report -m
"""

import pytest

from bus_transit_fare import (
    inspect_smartcard_turnstiles,
    process_commute_manifest,
)


def make_manifest(route_type="local", commuters=None, active=True,
                  priority=False):
    """Build a manifest dictionary with sensible defaults."""
    return {
        "route_active": active,
        "route_type": route_type,
        "priority_boarding": priority,
        "commuters": commuters if commuters is not None else [],
    }


def commuter(zones=1, kind="regular", blacklisted=False):
    """Build a commuter dictionary."""
    return {"zones": zones, "type": kind, "blacklisted": blacklisted}


# ---------- process_commute_manifest ----------

def test_single_regular_local_ride():
    manifests = [make_manifest("local", [commuter(2)])]
    result = process_commute_manifest(manifests, 2.0)
    assert result == {"total_fare": 4.5, "status": "COMPLETED"}


def test_manifests_must_be_a_list():
    with pytest.raises(ValueError):
        process_commute_manifest("not a list", 1.0)


def test_negative_booking_fee_is_rejected():
    with pytest.raises(ValueError):
        process_commute_manifest([], -1.0)


def test_inactive_route_is_skipped():
    manifests = [make_manifest("express", [commuter(2)], active=False)]
    result = process_commute_manifest(manifests, 1.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_express_student_gets_half_price():
    manifests = [make_manifest("express", [commuter(2, "student")])]
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_unknown_route_type_is_rejected():
    manifests = [make_manifest("ferry", [commuter(1)])]
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_zero_zone_commuter_is_rejected():
    manifests = [make_manifest("local", [commuter(0), commuter(1)])]
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_blacklisted_card_on_express_voids_the_whole_manifest():
    express = make_manifest(
        "express",
        [commuter(1), commuter(1, blacklisted=True), commuter(1)],
    )
    local = make_manifest("local", [commuter(1)])
    result = process_commute_manifest([express, local], 0.0)
    # The express manifest earns nothing; only the local ride is counted.
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_priority_boarding_adds_the_booking_fee():
    manifests = [make_manifest("local", [commuter(1)], priority=True)]
    result = process_commute_manifest(manifests, 2.0)
    assert result == {"total_fare": 5.5, "status": "COMPLETED"}


# ---------- inspect_smartcard_turnstiles ----------

def test_no_turnstile_data():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"


def test_two_failures_in_a_row_means_jam():
    assert inspect_smartcard_turnstiles([[0, 4, 5]]) == "TURNSTILE_JAM"


def test_streak_resets_after_a_good_reading():
    assert inspect_smartcard_turnstiles([[1, 2], [4, 0, 4]]) == "OPERATIONAL"
