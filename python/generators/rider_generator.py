from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

import pandas as pd
from faker import Faker


fake = Faker("en_IN")

OUTPUT_DIR = Path("data/riders")
RECORD_COUNT = 1_000


def generate_riders(count: int) -> pd.DataFrame:
    rows = []

    start_date = datetime(2024, 1, 1)

    for _ in range(count):
        rider_id = f"R{uuid.uuid4().hex[:10].upper()}"

        created_at = start_date + timedelta(
            days=random.randint(0, 900),
            seconds=random.randint(0, 86399),
        )

        updated_at = created_at

        rows.append(
            {
                "rider_id": rider_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.email(),
                "phone_number": fake.unique.msisdn()[:10],
                "date_of_birth": fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=65,
                ),
                "gender": random.choice(["M", "F", "OTHER"]),
                "signup_date": created_at,
                "home_location_id": None,
                "rider_status": random.choices(
                    ["ACTIVE", "INACTIVE", "SUSPENDED"],
                    weights=[85, 10, 5],
                )[0],
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

    return pd.DataFrame(rows)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_riders(RECORD_COUNT)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = OUTPUT_DIR / f"riders_{timestamp}.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df):,} riders")
    print(f"File: {output_file}")


if __name__ == "__main__":
    main()