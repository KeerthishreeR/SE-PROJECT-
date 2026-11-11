"""Campus parking permit manager: issue, revoke and check zone permits."""
import json
import secrets
from datetime import datetime, timedelta

# Shared state: all permits, keyed by vehicle plate.
PERMITS = {}
ZONES = ("A", "B", "C")
DATE_FORMAT = "%Y-%m-%d"
PERMIT_VALIDITY_DAYS = 180
DEFAULT_DB_FILE = "permits.json"

def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Issue a permit. Return the permit number, or None if the input is invalid."""
    if zone_records is None:
        zone_records = []
    if not isinstance(vehicle_plate, str) or not vehicle_plate.strip():
        return None
    if zone_id not in ZONES:
        return None
    permit_no = f"P{secrets.randbelow(90000) + 10000}"
    expiry = datetime.now() + timedelta(days=PERMIT_VALIDITY_DAYS)
    PERMITS[vehicle_plate] = {"zone": zone_id, "permit": permit_no, "expiry": expiry.strftime(DATE_FORMAT)}
    zone_records.append((vehicle_plate, zone_id))
    return permit_no

def revoke_permit(vehicle_plate):
    """Remove a permit. Return True if one existed, False otherwise."""
    return PERMITS.pop(vehicle_plate, None) is not None

def is_expired(vehicle_plate):
    """Return True if the plate's permit has expired or its date is unreadable."""
    permit = PERMITS.get(vehicle_plate)
    if permit is None:
        return False
    try:
        expiry = datetime.strptime(permit["expiry"], DATE_FORMAT)
    except (KeyError, ValueError):
        return True  # unreadable expiry: fail safe and treat as expired
    return expiry < datetime.now()

def scan_zone(zone_id, plates_seen):
    """Return the plates that should not be parked in the given zone."""
    flagged = []
    for plate in plates_seen:
        if plate not in PERMITS or PERMITS[plate]["zone"] != zone_id or is_expired(plate):
            flagged.append(plate)
    return flagged

def load_permit_database(file=DEFAULT_DB_FILE):
    """Load permits from a JSON file; start empty if it is missing or corrupt."""
    PERMITS.clear()
    try:
        with open(file, encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return
    except ValueError:
        print(f"Warning: {file} is not valid JSON; starting with no permits.")
        return
    if isinstance(data, dict):
        PERMITS.update(data)

def save_permit_database(file=DEFAULT_DB_FILE):
    """Write all permits to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(PERMITS, handle)

def set_expiry(vehicle_plate, date_text):
    """Set a permit's expiry (YYYY-MM-DD). Return True on success."""
    if vehicle_plate not in PERMITS:
        return False
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        return False
    PERMITS[vehicle_plate]["expiry"] = date_text
    return True

def main():
    """Run a small demo of the permit manager."""
    load_permit_database()
    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")  # invalid zone: rejected
    register_permit("", "B")  # empty plate: rejected
    register_permit(None, "C")  # missing plate: rejected
    set_expiry("KA01AB1234", "2020-01-01")
    revoke_permit("MH12ZZ0000")
    print("Flagged in zone A:", scan_zone("A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]))
    plate = input("Plate to revoke (Enter to skip): ").strip()
    if plate:
        revoke_permit(plate)
    save_permit_database()
    print("Permits on file:", len(PERMITS))

if __name__ == "__main__":
    main()
