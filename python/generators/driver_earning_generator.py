from pathlib import Path
from datetime import datetime
import random
import uuid

import pandas as pd


OUTPUT_DIR = Path("data/driver_earnings")
TRIP_DATA_DIR = Path("data/trips")


def get_latest_file(directory: Path) -> Path:
    files = sorted(directory.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {directory}"
        )

    return files[-1]


def generate_earnings(trips):

    rows = []

    completed_trips = trips[
        (trips["trip_status"] == "COMPLETED")
        & trips["driver_id"].notna()
    ].copy()

    for _, trip in completed_trips.iterrows():

        total_fare = float(trip["total_fare"])
        surge_amount = float(trip["surge_amount"])

        # --------------------------------------------------
        # TRIP FARE
        # --------------------------------------------------

        commission_rate = random.uniform(
            0.18,
            0.28
        )

        platform_commission = round(
            total_fare * commission_rate,
            2
        )

        driver_base_earning = round(
            total_fare - platform_commission,
            2
        )

        surge_earning = round(
            surge_amount * random.uniform(
                0.70,
                1.00
            ),
            2
        )

        net_driver_earning = round(
            driver_base_earning + surge_earning,
            2
        )

        earning_timestamp = pd.to_datetime(
            trip["completed_at"]
        )

        rows.append({
            "earning_id": (
                f"EARN{uuid.uuid4().hex[:10].upper()}"
            ),
            "trip_id": trip["trip_id"],
            "driver_id": trip["driver_id"],
            "earning_type": "TRIP_FARE",
            "gross_fare": total_fare,
            "platform_commission": platform_commission,
            "driver_base_earning": driver_base_earning,
            "surge_earning": surge_earning,
            "incentive_amount": 0.00,
            "adjustment_amount": 0.00,
            "net_driver_earning": net_driver_earning,
            "earning_status": random.choice([
                "CALCULATED",
                "APPROVED",
                "PAID",
            ]),
            "earning_timestamp": earning_timestamp,
            "created_at": earning_timestamp,
            "updated_at": earning_timestamp,
        })

        # --------------------------------------------------
        # OCCASIONAL INCENTIVE
        # --------------------------------------------------

        if random.random() < 0.15:

            incentive = round(
                random.uniform(50, 300),
                2
            )

            rows.append({
                "earning_id": (
                    f"EARN{uuid.uuid4().hex[:10].upper()}"
                ),
                "trip_id": trip["trip_id"],
                "driver_id": trip["driver_id"],
                "earning_type": "INCENTIVE",
                "gross_fare": None,
                "platform_commission": 0.00,
                "driver_base_earning": 0.00,
                "surge_earning": 0.00,
                "incentive_amount": incentive,
                "adjustment_amount": 0.00,
                "net_driver_earning": incentive,
                "earning_status": random.choice([
                    "CALCULATED",
                    "APPROVED",
                    "PAID",
                ]),
                "earning_timestamp": earning_timestamp,
                "created_at": earning_timestamp,
                "updated_at": earning_timestamp,
            })

    return pd.DataFrame(rows)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    trip_file = get_latest_file(
        TRIP_DATA_DIR
    )

    trips = pd.read_csv(
        trip_file
    )

    df = generate_earnings(
        trips
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR
        / f"driver_earnings_{timestamp}.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Generated {len(df):,} earnings records"
    )

    print(
        f"Unique drivers: "
        f"{df['driver_id'].nunique():,}"
    )

    print("\nEarning types:")
    print(
        df["earning_type"].value_counts()
    )

    print("\nEarning statuses:")
    print(
        df["earning_status"].value_counts()
    )

    print(
        f"\nFile: {output_file}"
    )


if __name__ == "__main__":
    main()