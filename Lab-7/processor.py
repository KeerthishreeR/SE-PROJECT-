"""Transit corridor, concession and passenger-density helpers.

Every function validates its input and reports a bad value with a
ValueError, so callers only have to handle one kind of failure.
"""

import math

BASE_FARE = 2.50
FARE_PER_ZONE = 0.75
MIN_ZONES = 1
MAX_ZONES = 99

DISCOUNTS = {
    "STANDARD": 1.00,
    "STUDENT": 0.50,
    "SENIOR": 0.35,
    "MILITARY": 0.20,
    "CHILD": 0.00,
}


def parse_transit_corridor(corridor_code):
    """Parse a code like "DT-UP-3" into a route description with its fare.

    Raises ValueError if the code is not text, does not have exactly three
    dash-separated parts, has an empty origin or destination, or if the zone
    count is not a whole number from 1 to 99.
    """
    if not isinstance(corridor_code, str):
        raise ValueError("corridor code must be text")

    parts = [part.strip() for part in corridor_code.strip().split("-")]
    if len(parts) != 3:
        raise ValueError("corridor code must look like ORIGIN-DEST-ZONES")
    orig, dest, zones_str = parts

    if not orig or not dest:
        raise ValueError("origin and destination must not be empty")
    if not (zones_str.isascii() and zones_str.isdigit()):
        raise ValueError("zones must be a whole number")

    zones = int(zones_str)
    if not MIN_ZONES <= zones <= MAX_ZONES:
        raise ValueError(f"zones must be between {MIN_ZONES} and {MAX_ZONES}")

    base_fare = BASE_FARE + (zones * FARE_PER_ZONE)
    return (f"Route {orig.upper()}->{dest.upper()}: "
            f"{zones} Zones, Fare ${base_fare:.2f}")


def lookup_concession_discount(category_name):
    """Return the fare multiplier for a concession category.

    Raises ValueError if the category is not text or is not a known category.
    """
    if not isinstance(category_name, str):
        raise ValueError("category must be text")

    category = category_name.strip().upper()
    if category not in DISCOUNTS:
        raise ValueError(f"unknown concession category: {category_name!r}")
    return DISCOUNTS[category]


def compute_passenger_density(occupancy_ratio_str):
    """Compute passengers per km from text such as "50/10.0".

    Raises ValueError if the input is not text, is not two numbers separated
    by "/", or if the numbers are not finite, the passenger count is
    negative or the distance is not greater than zero.
    """
    if not isinstance(occupancy_ratio_str, str):
        raise ValueError("ratio must be text")

    parts = occupancy_ratio_str.split("/")
    if len(parts) != 2:
        raise ValueError("ratio must look like PASSENGERS/KM")

    passengers = float(parts[0])  # float() itself raises ValueError
    km = float(parts[1])

    if not (math.isfinite(passengers) and math.isfinite(km)):
        raise ValueError("passengers and km must be finite numbers")
    if passengers < 0:
        raise ValueError("passengers must not be negative")
    if km <= 0:
        raise ValueError("km must be greater than zero")

    density = passengers / km
    if not math.isfinite(density):
        raise ValueError("density is too large to represent")
    return round(density, 2)


def main():
    """Ask for one value per function and show the result or the error."""
    print("==== Running parse_transit_corridor ====")
    c_input = input("Enter corridor (e.g. DT-UP-3): ")
    try:
        print(parse_transit_corridor(c_input))
    except ValueError as error:
        print("Invalid corridor:", error)

    print("\n==== Running lookup_concession_discount ====")
    cat_input = input("Enter concession category (e.g. STUDENT, SENIOR): ")
    try:
        print("Multiplier:", lookup_concession_discount(cat_input))
    except ValueError as error:
        print("Invalid category:", error)

    print("\n==== Running compute_passenger_density ====")
    d_input = input("Enter passengers/km (e.g. 50/10.0): ")
    try:
        print("Density:", compute_passenger_density(d_input))
    except ValueError as error:
        print("Invalid ratio:", error)


if __name__ == "__main__":
    main()
