from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

import pandas as pd


OUTPUT_DIR = Path("data/driver_vehicle_assignments")

DRIVER_DATA_DIR = Path("data/drivers")
VEHICLE_DATA_DIR = Path("data/vehicles")

RECORD_COUNT = 600


ASSIGNMENT_REASONS = [
    "INITIAL_ASSIGNMENT",
    "VEHICLE_CHANGE",
    "VEHICLE_MAINTENANCE",
    "DRIVER_CHANGE",
    "VEHICLE_REPLACEMENT",
]


def get_latest_file(directory: Path) -> Path:
    files = sorted(directory.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {directory}"
        )

    return files[-1]


def generate_assignments(
    drivers: pd.DataFrame,
    vehicles: pd.DataFrame,
    count: int,
) -> pd.DataFrame:

    rows = []

    driver_ids = drivers["driver_id"].tolist()
    vehicle_ids = vehicles["vehicle_id"].tolist()

    used_pairs = set()

    while len(rows) < count:

        driver_id = random.choice(driver_ids)
        vehicle_id = random.choice(vehicle_ids)

        pair = (driver_id, vehicle_id)

        if pair in used_pairs:
            continue

        used_pairs.add(pair)

        assigned_at = datetime.now() - timedelta(
            days=random.randint(1, 900),
            hours=random.randint(0, 23),
        )

        is_current = random.random() < 0.70

        if is_current:
            unassigned_at = None
            assignment_status = "ACTIVE"
            assignment_reason = "INITIAL_ASSIGNMENT"
        else:
            unassigned_at = assigned_at + timedelta(
                days=random.randint(10, 300),
            )

            assignment_status = random.choice(
                ["ENDED", "SUSPENDED"]
            )

            assignment_reason = random.choice(
                [
                    "VEHICLE_CHANGE",
                    "VEHICLE_MAINTENANCE",
                    "DRIVER_CHANGE",
                    "VEHICLE_REPLACEMENT",
                ]
            )

        created_at = assigned_at
        updated_at = (
            datetime.now()
            if unassigned_at is not None
            else assigned_at
        )

        rows.append(
            {
                "assignment_id": (
                    f"A{uuid.uuid4().hex[:10].upper()}"
                ),
                "driver_id": driver_id,
                "vehicle_id": vehicle_id,
                "assigned_at": assigned_at,
                "unassigned_at": unassigned_at,
                "assignment_status": assignment_status,
                "assignment_reason": assignment_reason,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

    return pd.DataFrame(rows)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    driver_file = get_latest_file(
        DRIVER_DATA_DIR
    )

    vehicle_file = get_latest_file(
        VEHICLE_DATA_DIR
    )

    drivers = pd.read_csv(driver_file)

    vehicles = pd.read_csv(vehicle_file)

    df = generate_assignments(
        drivers,
        vehicles,
        RECORD_COUNT,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR
        / f"driver_vehicle_assignments_{timestamp}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"Generated {len(df):,} assignments"
    )

    print(
        f"Drivers used: "
        f"{df['driver_id'].nunique():,}"
    )

    print(
        f"Vehicles used: "
        f"{df['vehicle_id'].nunique():,}"
    )

    print(
        f"File: {output_file}"
    )


if __name__ == "__main__":
    main()