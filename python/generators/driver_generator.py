from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

import pandas as pd
from faker import Faker


fake = Faker("en_IN")

OUTPUT_DIR = Path("data/drivers")
RECORD_COUNT = 500


def generate_drivers(count: int) -> pd.DataFrame:
    rows = []

    start_date = datetime(2022, 1, 1)

    for _ in range(count):
        driver_id = f"D{uuid.uuid4().hex[:10].upper()}"

        joining_at = start_date + timedelta(
            days=random.randint(0, 1700),
            seconds=random.randint(0, 86399),
        )

        created_at = joining_at
        updated_at = created_at

        license_expiry_date = (
            joining_at.date()
            + timedelta(days=random.randint(730, 1825))
        )

        rows.append(
            {
                "driver_id": driver_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.email(),
                "phone_number": fake.unique.msisdn()[:10],
                "license_number": (
                    f"LIC-{uuid.uuid4().hex[:10].upper()}"
                ),
                "license_expiry_date": license_expiry_date,
                "joining_date": joining_at.date(),
                "home_location_id": None,
                "driver_status": random.choices(
                    [
                        "ACTIVE",
                        "INACTIVE",
                        "SUSPENDED",
                        "DEACTIVATED",
                        "PENDING",
                    ],
                    weights=[80, 7, 5, 3, 5],
                )[0],
                "driver_tier": random.choices(
                    [
                        "STANDARD",
                        "PREMIUM",
                        "ELITE",
                    ],
                    weights=[70, 20, 10],
                )[0],
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

    return pd.DataFrame(rows)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_drivers(RECORD_COUNT)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"drivers_{timestamp}.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df):,} drivers")
    print(f"File: {output_file}")


if __name__ == "__main__":
    main()