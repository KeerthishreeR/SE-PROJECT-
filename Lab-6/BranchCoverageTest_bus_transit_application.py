"""Lab 6 - tests written to reach (at least) 90% BRANCH coverage.

Every decision in bus_transit_fare.py is exercised for both its True and
False outcome. Run from the Lab-6 folder:

    coverage run --branch -m pytest BranchCoverageTest_bus_transit_application.py
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


# ---------- input validation (decision: not list OR fee < 0) ----------

def test_manifests_must_be_a_list():
    with pytest.raises(ValueError):
        process_commute_manifest("not a list", 1.0)


def test_negative_booking_fee_is_rejected():
    with pytest.raises(ValueError):
        process_commute_manifest([], -0.01)


def test_zero_booking_fee_is_allowed():
    assert process_commute_manifest([], 0.0) == {
        "total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_empty_manifest_list_means_zero_ridership():
    assert process_commute_manifest([], 5.0) == {
        "total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


# ---------- route_active (True / False) ----------

def test_active_route_is_charged():
    result = process_commute_manifest([make_manifest("local", [commuter(2)])], 2.0)
    assert result == {"total_fare": 4.5, "status": "COMPLETED"}


def test_inactive_route_is_skipped():
    manifests = [make_manifest("express", [commuter(2)], active=False)]
    result = process_commute_manifest(manifests, 1.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_missing_route_active_defaults_to_inactive():
    result = process_commute_manifest([{"commuters": [commuter(1)]}], 0.0)
    assert result["status"] == "ZERO_RIDERSHIP"


# ---------- route type (express / shuttle / local / unknown) ----------

def test_express_base_fare():
    result = process_commute_manifest([make_manifest("express", [commuter(1)])], 0.0)
    assert result["total_fare"] == 7.0


def test_shuttle_base_fare():
    result = process_commute_manifest([make_manifest("shuttle", [commuter(1)])], 0.0)
    assert result["total_fare"] == 5.0


def test_local_base_fare():
    result = process_commute_manifest([make_manifest("local", [commuter(1)])], 0.0)
    assert result["total_fare"] == 3.5


def test_missing_route_type_defaults_to_local():
    manifest = {"route_active": True, "commuters": [commuter(1)]}
    assert process_commute_manifest([manifest], 0.0)["total_fare"] == 3.5


def test_unknown_route_type_is_rejected():
    manifests = [make_manifest("ferry", [commuter(1)])]
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


# ---------- zones (<= 0 rejected, > 0 charged) ----------

def test_zero_zone_commuter_is_rejected():
    manifests = [make_manifest("local", [commuter(0), commuter(1)])]
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_negative_zone_commuter_is_rejected():
    manifests = [make_manifest("local", [commuter(-3)])]
    assert process_commute_manifest(manifests, 0.0)["status"] == "ZERO_RIDERSHIP"


def test_missing_zones_default_to_one():
    manifests = [make_manifest("local", [{"type": "regular"}])]
    assert process_commute_manifest(manifests, 0.0)["total_fare"] == 3.5


# ---------- passenger type (student / senior / regular / other) ----------

def test_express_student_gets_half_price():
    manifests = [make_manifest("express", [commuter(2, "student")])]
    assert process_commute_manifest(manifests, 0.0)["total_fare"] == 3.5


def test_shuttle_senior_gets_thirty_percent_off():
    manifests = [make_manifest("shuttle", [commuter(4, "senior")])]
    assert process_commute_manifest(manifests, 0.0)["total_fare"] == 4.2


def test_unknown_passenger_type_pays_the_regular_fare():
    manifests = [make_manifest("local", [commuter(2, "child")])]
    assert process_commute_manifest(manifests, 0.0)["total_fare"] == 4.5


def test_missing_passenger_type_defaults_to_regular():
    manifests = [make_manifest("local", [{"zones": 2}])]
    assert process_commute_manifest(manifests, 0.0)["total_fare"] == 4.5


# ---------- blacklisted card (express voids the manifest) ----------

def test_blacklisted_card_on_express_voids_the_whole_manifest():
    express = make_manifest(
        "express",
        [commuter(1), commuter(1, blacklisted=True), commuter(1)],
    )
    local = make_manifest("local", [commuter(1)])
    result = process_commute_manifest([express, local], 0.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_blacklisted_card_on_local_only_skips_that_commuter():
    manifests = [
        make_manifest("local", [commuter(1), commuter(1, "regular", True)])
    ]
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_express_void_still_charges_booking_fee_when_priority():
    manifests = [
        make_manifest("express", [commuter(1, blacklisted=True)],
                      priority=True)
    ]
    result = process_commute_manifest(manifests, 2.0)
    assert result == {"total_fare": 2.0, "status": "COMPLETED"}


# ---------- priority boarding (True / False) ----------

def test_priority_boarding_adds_the_booking_fee():
    manifests = [make_manifest("local", [commuter(1)], priority=True)]
    result = process_commute_manifest(manifests, 2.0)
    assert result == {"total_fare": 5.5, "status": "COMPLETED"}


def test_no_priority_boarding_means_no_fee():
    manifests = [make_manifest("local", [commuter(1)], priority=False)]
    result = process_commute_manifest(manifests, 2.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_manifest_without_commuters_is_free():
    result = process_commute_manifest([make_manifest("local", [])], 2.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


# ---------- audit rule (rejected_rides > 4) ----------

def test_four_rejections_do_not_fail_the_audit():
    manifests = [make_manifest("ferry", [commuter(1)]) for _ in range(4)]
    manifests.append(make_manifest("local", [commuter(1)]))
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_five_rejections_fail_the_audit():
    manifests = [make_manifest("ferry", [commuter(1)]) for _ in range(5)]
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 0.0, "status": "AUDIT_REJECTED"}


def test_audit_rejection_keeps_the_fare_collected_so_far():
    manifests = [make_manifest("local", [commuter(1)])]
    manifests += [make_manifest("ferry", [commuter(1)]) for _ in range(5)]
    result = process_commute_manifest(manifests, 0.0)
    assert result == {"total_fare": 3.5, "status": "AUDIT_REJECTED"}


# ---------- inspect_smartcard_turnstiles ----------

def test_no_turnstile_data():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"


def test_two_failures_in_a_row_means_jam():
    assert inspect_smartcard_turnstiles([[0, 4, 5]]) == "TURNSTILE_JAM"


def test_streak_resets_after_a_good_reading():
    assert inspect_smartcard_turnstiles([[4, 0, 4]]) == "OPERATIONAL"


def test_three_failures_is_not_enough_to_count():
    assert inspect_smartcard_turnstiles([[3, 3, 3]]) == "OPERATIONAL"


def test_streak_does_not_carry_over_between_devices():
    assert inspect_smartcard_turnstiles([[0, 5], [5, 0]]) == "OPERATIONAL"


def test_jam_on_a_later_device_is_found():
    assert inspect_smartcard_turnstiles([[0, 0], [5, 5]]) == "TURNSTILE_JAM"


def test_device_with_no_readings_is_fine():
    assert inspect_smartcard_turnstiles([[]]) == "OPERATIONAL"
