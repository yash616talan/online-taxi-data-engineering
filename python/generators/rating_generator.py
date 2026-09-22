from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

import pandas as pd


OUTPUT_DIR = Path("data/ratings")

TRIP_DATA_DIR = Path("data/trips")

RECORD_COUNT = 2_200


RATING_COMMENTS = [
    "Great experience",
    "Very professional",
    "Smooth ride",
    "Good driver",
    "Clean vehicle",
    "Friendly and polite",
    "Arrived on time",
    "Safe driving",
    "Average experience",
    "Could be better",
    "Long wait time",
    "Driver was helpful",
]


def get_latest_file(directory: Path) -> Path:
    files = sorted(directory.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {directory}"
        )

    return files[-1]


def create_rating(
    trip,
    rater_type,
    rating_value,
    rating_comment,
):
    if rater_type == "RIDER":
        rater_id = trip["rider_id"]
        rated_entity_type = "DRIVER"
        rated_entity_id = trip["driver_id"]
    else:
        rater_id = trip["driver_id"]
        rated_entity_type = "RIDER"
        rated_entity_id = trip["rider_id"]

    completed_at = pd.to_datetime(
        trip["completed_at"]
    )

    rating_timestamp = (
        completed_at
        + timedelta(
            minutes=random.randint(1, 1440)
        )
    )

    return {
        "rating_id": (
            f"RAT{uuid.uuid4().hex[:10].upper()}"
        ),
        "trip_id": trip["trip_id"],
        "rater_type": rater_type,
        "rater_id": rater_id,
        "rated_entity_type": rated_entity_type,
        "rated_entity_id": rated_entity_id,
        "rating_value": rating_value,
        "rating_comment": rating_comment,
        "rating_timestamp": rating_timestamp,
        "created_at": rating_timestamp,
        "updated_at": rating_timestamp,
    }


def generate_ratings(trips):

    completed_trips = trips[
        trips["trip_status"] == "COMPLETED"
    ].copy()

    # A rating requires both a rider and driver.
    completed_trips = completed_trips[
        completed_trips["rider_id"].notna()
        & completed_trips["driver_id"].notna()
    ]

    rows = []

    for _, trip in completed_trips.iterrows():

        # -----------------------------------------------------
        # Rider → Driver
        # -----------------------------------------------------

        if random.random() < 0.70:

            rating_value = random.choices(
                [1, 2, 3, 4, 5],
                weights=[
                    3,
                    5,
                    12,
                    30,
                    50,
                ],
            )[0]

            rows.append(
                create_rating(
                    trip=trip,
                    rater_type="RIDER",
                    rating_value=rating_value,
                    rating_comment=random.choice(
                        RATING_COMMENTS
                    ),
                )
            )

        # -----------------------------------------------------
        # Driver → Rider
        # -----------------------------------------------------

        if random.random() < 0.55:

            rating_value = random.choices(
                [1, 2, 3, 4, 5],
                weights=[
                    2,
                    5,
                    15,
                    32,
                    46,
                ],
            )[0]

            rows.append(
                create_rating(
                    trip=trip,
                    rater_type="DRIVER",
                    rating_value=rating_value,
                    rating_comment=random.choice(
                        RATING_COMMENTS
                    ),
                )
            )

    return pd.DataFrame(rows)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    trip_file = get_latest_file(
        TRIP_DATA_DIR
    )

    trips = pd.read_csv(
        trip_file
    )

    df = generate_ratings(
        trips
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR
        / f"ratings_{timestamp}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"Generated {len(df):,} ratings"
    )

    print(
        f"Trips rated: "
        f"{df['trip_id'].nunique():,}"
    )

    print("\nRater distribution:")

    print(
        df["rater_type"].value_counts()
    )

    print("\nRating distribution:")

    print(
        df["rating_value"].value_counts()
        .sort_index()
    )

    print(
        f"\nFile: {output_file}"
    )


if __name__ == "__main__":
    main()