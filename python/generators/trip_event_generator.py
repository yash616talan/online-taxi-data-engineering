from pathlib import Path
from datetime import datetime
import uuid

import pandas as pd


OUTPUT_DIR = Path("data/trip_events")
TRIP_DATA_DIR = Path("data/trips")


def get_latest_file(directory: Path) -> Path:
    files = sorted(directory.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {directory}"
        )

    return files[-1]


def create_event(
    trip,
    event_type,
    event_timestamp,
    event_sequence,
):
    return {
        "event_id": f"E{uuid.uuid4().hex[:10].upper()}",
        "trip_id": trip["trip_id"],
        "event_type": event_type,
        "event_timestamp": event_timestamp,
        "event_sequence": event_sequence,
        "driver_id": trip["driver_id"],
        "vehicle_id": trip["vehicle_id"],
        "location_id": (
            trip["pickup_location_id"]
            if event_type in [
                "TRIP_REQUESTED",
                "DRIVER_ASSIGNED",
            ]
            else trip["dropoff_location_id"]
        ),
        "event_source": "TRIP_SERVICE",
        "created_at": event_timestamp,
    }


def generate_trip_events(trips):
    rows = []

    for _, trip in trips.iterrows():

        events = []

        # -----------------------------------------------------
        # TRIP REQUESTED
        # -----------------------------------------------------

        events.append(
            (
                "TRIP_REQUESTED",
                trip["requested_at"],
            )
        )

        # -----------------------------------------------------
        # DRIVER ASSIGNED
        # -----------------------------------------------------

        if pd.notna(trip["driver_id"]):

            if pd.notna(trip["accepted_at"]):

                events.append(
                    (
                        "DRIVER_ASSIGNED",
                        trip["accepted_at"],
                    )
                )

        # -----------------------------------------------------
        # DRIVER ARRIVING
        # -----------------------------------------------------

        if pd.notna(trip["driver_arrived_at"]):

            events.append(
                (
                    "DRIVER_ARRIVING",
                    trip["driver_arrived_at"],
                )
            )

        # -----------------------------------------------------
        # TRIP STARTED
        # -----------------------------------------------------

        if pd.notna(trip["started_at"]):

            events.append(
                (
                    "TRIP_STARTED",
                    trip["started_at"],
                )
            )

        # -----------------------------------------------------
        # COMPLETED / CANCELLED
        # -----------------------------------------------------

        if trip["trip_status"] == "COMPLETED":

            if pd.notna(trip["completed_at"]):

                events.append(
                    (
                        "TRIP_COMPLETED",
                        trip["completed_at"],
                    )
                )

        elif trip["trip_status"] in [
            "CANCELLED_BY_RIDER",
            "CANCELLED_BY_DRIVER",
            "NO_DRIVER_FOUND",
        ]:

            if pd.notna(trip["cancelled_at"]):

                events.append(
                    (
                        "TRIP_CANCELLED",
                        trip["cancelled_at"],
                    )
                )

        # -----------------------------------------------------
        # Create event rows
        # -----------------------------------------------------

        events.sort(key=lambda x: pd.to_datetime(x[1]))

        for sequence, (
            event_type,
            event_timestamp,
        ) in enumerate(events, start=1):

            rows.append(
                create_event(
                    trip=trip,
                    event_type=event_type,
                    event_timestamp=event_timestamp,
                    event_sequence=sequence,
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

    df = generate_trip_events(
        trips
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR
        / f"trip_events_{timestamp}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"Generated {len(df):,} trip events"
    )

    print(
        f"Trips represented: "
        f"{df['trip_id'].nunique():,}"
    )

    print("\nEvent distribution:")

    print(
        df["event_type"].value_counts()
    )

    print(
        f"\nFile: {output_file}"
    )


if __name__ == "__main__":
    main()