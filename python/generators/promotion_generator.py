from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

import pandas as pd


OUTPUT_DIR = Path("data/promotions")
RECORD_COUNT = 50


PROMOTION_TYPES = [
    "PERCENTAGE",
    "FIXED_AMOUNT",
    "FREE_RIDE",
]

PROMOTION_STATUSES = [
    "SCHEDULED",
    "ACTIVE",
    "EXPIRED",
    "CANCELLED",
]


def generate_promotions(count: int) -> pd.DataFrame:
    rows = []

    base_date = datetime.now() - timedelta(days=180)

    for i in range(count):
        promotion_id = f"P{uuid.uuid4().hex[:10].upper()}"

        promotion_type = random.choice(PROMOTION_TYPES)

        start_at = base_date + timedelta(
            days=i * 5
        )

        end_at = start_at + timedelta(
            days=random.randint(7, 45)
        )

        if end_at < datetime.now():
            promotion_status = "EXPIRED"
        elif start_at > datetime.now():
            promotion_status = "SCHEDULED"
        else:
            promotion_status = "ACTIVE"

        if promotion_type == "PERCENTAGE":
            discount_value = random.choice(
                [10, 15, 20, 25, 30]
            )
            max_discount_amount = random.choice(
                [50, 100, 150, 200]
            )

        elif promotion_type == "FIXED_AMOUNT":
            discount_value = random.choice(
                [50, 75, 100, 150, 200]
            )
            max_discount_amount = None

        else:
            discount_value = 100
            max_discount_amount = None

        min_trip_amount = random.choice(
            [0, 100, 200, 300, 500]
        )

        created_at = start_at
        updated_at = created_at

        rows.append(
            {
                "promotion_id": promotion_id,
                "promotion_code": f"RIDE{i + 1:04d}",
                "promotion_name": (
                    f"Ride Promotion {i + 1}"
                ),
                "promotion_type": promotion_type,
                "discount_value": discount_value,
                "max_discount_amount": max_discount_amount,
                "min_trip_amount": min_trip_amount,
                "start_at": start_at,
                "end_at": end_at,
                "usage_limit": random.choice(
                    [100, 500, 1000, 5000, None]
                ),
                "promotion_status": promotion_status,
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

    df = generate_promotions(RECORD_COUNT)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR
        / f"promotions_{timestamp}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"Generated {len(df):,} promotions"
    )

    print(
        f"File: {output_file}"
    )


if __name__ == "__main__":
    main()