from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

import pandas as pd


OUTPUT_DIR = Path("data/trips")

DATA_DIRS = {
    "riders": Path("data/riders"),
    "drivers": Path("data/drivers"),
    "vehicles": Path("data/vehicles"),
    "locations": Path("data/locations"),
    "promotions": Path("data/promotions"),
    "assignments": Path("data/driver_vehicle_assignments"),
}

RECORD_COUNT = 2_000


TRIP_STATUSES = [
    "COMPLETED",
    "CANCELLED_BY_RIDER",
    "CANCELLED_BY_DRIVER",
    "NO_DRIVER_FOUND",
]

CANCELLATION_REASONS = [
    "RIDER_CHANGED_PLANS",
    "DRIVER_TOO_FAR",
    "DRIVER_CANCELLED",
    "PAYMENT_ISSUE",
    "NO_DRIVER_AVAILABLE",
]


def get_latest_file(directory: Path) -> Path:
    """Return the most recently generated CSV from a directory."""

    files = sorted(directory.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {directory}"
        )

    return files[-1]


def load_data():
    """Load the latest source CSV for each required entity."""

    data = {}

    for name, directory in DATA_DIRS.items():
        file = get_latest_file(directory)
        data[name] = pd.read_csv(file)

    return data


def generate_trip(
    rider_id,
    driver_id,
    vehicle_id,
    pickup_location_id,
    dropoff_location_id,
    promotion_id,
):
    """
    Generate one realistic trip.

    Driver and vehicle are passed into this function based on
    an actual driver-vehicle assignment.

    NO_DRIVER_FOUND trips will explicitly clear both IDs.
    """

    requested_at = datetime.now() - timedelta(
        days=random.randint(1, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )

    status = random.choices(
        TRIP_STATUSES,
        weights=[80, 7, 6, 7],
    )[0]

    accepted_at = None
    driver_arrived_at = None
    started_at = None
    completed_at = None
    cancelled_at = None
    cancellation_reason = None

    # Default duration
    duration_minutes = 0

    # ---------------------------------------------------------
    # COMPLETED
    # ---------------------------------------------------------

    if status == "COMPLETED":

        # A completed trip MUST have a driver and vehicle.
        if driver_id is None or vehicle_id is None:
            raise ValueError(
                "Completed trip cannot have NULL driver_id "
                "or vehicle_id."
            )

        accepted_at = requested_at + timedelta(
            minutes=random.randint(1, 5)
        )

        driver_arrived_at = accepted_at + timedelta(
            minutes=random.randint(3, 12)
        )

        started_at = driver_arrived_at + timedelta(
            minutes=random.randint(1, 5)
        )

        duration_minutes = random.uniform(
            8,
            90,
        )

        completed_at = started_at + timedelta(
            minutes=duration_minutes
        )

    # ---------------------------------------------------------
    # CANCELLED BY RIDER
    # ---------------------------------------------------------

    elif status == "CANCELLED_BY_RIDER":

        cancelled_at = requested_at + timedelta(
            minutes=random.randint(2, 20)
        )

        cancellation_reason = random.choice(
            [
                "RIDER_CHANGED_PLANS",
                "PAYMENT_ISSUE",
            ]
        )

        # Sometimes rider cancels before a driver accepts.
        # Sometimes a driver has already been assigned.
        if driver_id is not None and random.random() < 0.70:

            accepted_at = requested_at + timedelta(
                minutes=random.randint(1, 5)
            )

            driver_arrived_at = (
                accepted_at
                + timedelta(
                    minutes=random.randint(3, 12)
                )
            )

    # ---------------------------------------------------------
    # CANCELLED BY DRIVER
    # ---------------------------------------------------------

    elif status == "CANCELLED_BY_DRIVER":

        # A driver cancellation requires an assigned driver.
        if driver_id is None or vehicle_id is None:
            raise ValueError(
                "Cancelled-by-driver trip cannot have NULL "
                "driver_id or vehicle_id."
            )

        accepted_at = requested_at + timedelta(
            minutes=random.randint(1, 5)
        )

        cancelled_at = accepted_at + timedelta(
            minutes=random.randint(2, 15)
        )

        cancellation_reason = random.choice(
            [
                "DRIVER_CANCELLED",
                "DRIVER_TOO_FAR",
            ]
        )

    # ---------------------------------------------------------
    # NO DRIVER FOUND
    # ---------------------------------------------------------

    elif status == "NO_DRIVER_FOUND":

        # No driver means no driver or vehicle.
        driver_id = None
        vehicle_id = None

        cancelled_at = requested_at + timedelta(
            minutes=random.randint(2, 10)
        )

        cancellation_reason = "NO_DRIVER_AVAILABLE"

        duration_minutes = 0

    # ---------------------------------------------------------
    # FARE CALCULATION
    # ---------------------------------------------------------

    distance_km = round(
        random.uniform(1, 35),
        3,
    )

    base_fare = round(
        60 + distance_km * random.uniform(10, 18),
        2,
    )

    surge_multiplier = random.choice(
        [
            0,
            0,
            0,
            0.10,
            0.20,
            0.30,
        ]
    )

    surge_amount = round(
        base_fare * surge_multiplier,
        2,
    )

    if promotion_id is not None:
        discount_amount = round(
            random.uniform(20, 100),
            2,
        )
    else:
        discount_amount = 0

    taxable_amount = max(
        base_fare
        + surge_amount
        - discount_amount,
        0,
    )

    tax_amount = round(
        taxable_amount * 0.05,
        2,
    )

    total_fare = round(
        taxable_amount + tax_amount,
        2,
    )

    # ---------------------------------------------------------
    # AUDIT TIMESTAMPS
    # ---------------------------------------------------------

    created_at = requested_at

    updated_at = (
        completed_at
        or cancelled_at
        or requested_at
    )

    return {
        "trip_id": (
            f"T{uuid.uuid4().hex[:10].upper()}"
        ),
        "rider_id": rider_id,
        "driver_id": driver_id,
        "vehicle_id": vehicle_id,
        "pickup_location_id": pickup_location_id,
        "dropoff_location_id": dropoff_location_id,
        "promotion_id": promotion_id,
        "trip_status": status,
        "requested_at": requested_at,
        "accepted_at": accepted_at,
        "driver_arrived_at": driver_arrived_at,
        "started_at": started_at,
        "completed_at": completed_at,
        "cancelled_at": cancelled_at,
        "cancellation_reason": cancellation_reason,
        "distance_km": distance_km,
        "duration_minutes": round(
            duration_minutes,
            2,
        ),
        "base_fare": base_fare,
        "surge_amount": surge_amount,
        "discount_amount": discount_amount,
        "tax_amount": tax_amount,
        "total_fare": total_fare,
        "created_at": created_at,
        "updated_at": updated_at,
    }


def generate_trips(data, count):
    """Generate a batch of trips using existing source IDs."""

    riders = data["riders"]
    locations = data["locations"]
    promotions = data["promotions"]
    assignments = data["assignments"]

    # Only active assignments are used when assigning
    # drivers and vehicles to trips.
    valid_assignments = assignments[
        assignments["assignment_status"] == "ACTIVE"
    ].copy()

    if valid_assignments.empty:
        raise ValueError(
            "No ACTIVE driver-vehicle assignments available."
        )

    rider_ids = riders["rider_id"].tolist()
    location_ids = locations["location_id"].tolist()
    promotion_ids = promotions["promotion_id"].tolist()

    rows = []

    for _ in range(count):

        # -----------------------------------------------------
        # Rider
        # -----------------------------------------------------

        rider_id = random.choice(rider_ids)

        # -----------------------------------------------------
        # Pickup / Dropoff
        # -----------------------------------------------------

        pickup_location_id = random.choice(
            location_ids
        )

        dropoff_location_id = random.choice(
            location_ids
        )

        # Avoid same pickup and dropoff.
        while (
            dropoff_location_id
            == pickup_location_id
        ):
            dropoff_location_id = random.choice(
                location_ids
            )

        # -----------------------------------------------------
        # Promotion
        # -----------------------------------------------------

        # Approximately 25% of trips use a promotion.
        if random.random() < 0.25:
            promotion_id = random.choice(
                promotion_ids
            )
        else:
            promotion_id = None

        # -----------------------------------------------------
        # Driver / Vehicle
        # -----------------------------------------------------

        # We initially select a valid active assignment.
        #
        # generate_trip() will remove the driver/vehicle
        # only when the final status becomes NO_DRIVER_FOUND.

        assignment = valid_assignments.sample(
            n=1
        ).iloc[0]

        driver_id = assignment["driver_id"]
        vehicle_id = assignment["vehicle_id"]

        # -----------------------------------------------------
        # Generate Trip
        # -----------------------------------------------------

        row = generate_trip(
            rider_id=rider_id,
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            pickup_location_id=pickup_location_id,
            dropoff_location_id=dropoff_location_id,
            promotion_id=promotion_id,
        )

        rows.append(row)

    return pd.DataFrame(rows)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = load_data()

    df = generate_trips(
        data,
        RECORD_COUNT,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR
        / f"trips_{timestamp}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    print(
        f"Generated {len(df):,} trips"
    )

    print("\nTrip status distribution:")

    print(
        df["trip_status"].value_counts()
    )

    print(
        f"\nTrips with drivers: "
        f"{df['driver_id'].notna().sum():,}"
    )

    print(
        f"Trips without drivers: "
        f"{df['driver_id'].isna().sum():,}"
    )

    print(
        f"Trips with promotions: "
        f"{df['promotion_id'].notna().sum():,}"
    )

    print(
        f"\nFile: {output_file}"
    )


if __name__ == "__main__":
    main()