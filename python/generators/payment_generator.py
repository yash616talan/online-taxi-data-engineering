from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

import pandas as pd


OUTPUT_DIR = Path("data/payments")

TRIP_DATA_DIR = Path("data/trips")

RECORD_COUNT = 2_300


PAYMENT_METHODS = [
    "CASH",
    "CREDIT_CARD",
    "DEBIT_CARD",
    "UPI",
    "WALLET",
]

PAYMENT_STATUSES = [
    "INITIATED",
    "PROCESSING",
    "SUCCESS",
    "FAILED",
    "REFUNDED",
]


FAILURE_REASONS = [
    "INSUFFICIENT_FUNDS",
    "CARD_DECLINED",
    "PAYMENT_TIMEOUT",
    "BANK_ERROR",
    "INVALID_PAYMENT_DETAILS",
]


def get_latest_file(directory: Path) -> Path:
    files = sorted(directory.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {directory}"
        )

    return files[-1]


def generate_payment(
    trip,
    payment_status,
    payment_method,
    payment_timestamp,
):
    amount = round(
        float(trip["total_fare"]),
        2,
    )

    payment_completed_at = None
    failure_reason = None

    if payment_status == "SUCCESS":

        payment_completed_at = (
            payment_timestamp
            + timedelta(
                seconds=random.randint(2, 60)
            )
        )

    elif payment_status == "FAILED":

        failure_reason = random.choice(
            FAILURE_REASONS
        )

    elif payment_status == "REFUNDED":

        payment_completed_at = (
            payment_timestamp
            + timedelta(
                seconds=random.randint(2, 60)
            )
        )

    transaction_reference = None

    if payment_status in [
        "SUCCESS",
        "REFUNDED",
    ]:

        transaction_reference = (
            f"TXN-{uuid.uuid4().hex[:12].upper()}"
        )

    return {
        "payment_id": (
            f"PAY{uuid.uuid4().hex[:10].upper()}"
        ),
        "trip_id": trip["trip_id"],
        "rider_id": trip["rider_id"],
        "payment_method": payment_method,
        "payment_status": payment_status,
        "transaction_reference": transaction_reference,
        "amount": amount,
        "currency": "INR",
        "payment_initiated_at": payment_timestamp,
        "payment_completed_at": payment_completed_at,
        "failure_reason": failure_reason,
        "created_at": payment_timestamp,
        "updated_at": (
            payment_completed_at
            or payment_timestamp
        ),
    }


def generate_payments(trips):
    rows = []

    # ---------------------------------------------------------
    # First generate payments for completed trips.
    # ---------------------------------------------------------

    completed_trips = trips[
        trips["trip_status"] == "COMPLETED"
    ].copy()

    for _, trip in completed_trips.iterrows():

        # Most completed trips succeed on the first attempt.
        if random.random() < 0.88:

            payment_timestamp = pd.to_datetime(
                trip["completed_at"]
            )

            payment = generate_payment(
                trip=trip,
                payment_status="SUCCESS",
                payment_method=random.choice(
                    PAYMENT_METHODS
                ),
                payment_timestamp=payment_timestamp,
            )

            rows.append(payment)

        else:

            # Failed first attempt.
            first_timestamp = pd.to_datetime(
                trip["completed_at"]
            )

            failed_payment = generate_payment(
                trip=trip,
                payment_status="FAILED",
                payment_method=random.choice(
                    PAYMENT_METHODS
                ),
                payment_timestamp=first_timestamp,
            )

            rows.append(failed_payment)

            # Most failed payments are retried successfully.
            if random.random() < 0.85:

                retry_timestamp = (
                    first_timestamp
                    + timedelta(
                        minutes=random.randint(1, 10)
                    )
                )

                successful_payment = generate_payment(
                    trip=trip,
                    payment_status="SUCCESS",
                    payment_method=random.choice(
                        PAYMENT_METHODS
                    ),
                    payment_timestamp=retry_timestamp,
                )

                rows.append(
                    successful_payment
                )

    # ---------------------------------------------------------
    # Cancelled trips
    # ---------------------------------------------------------

    cancelled_trips = trips[
        trips["trip_status"].isin(
            [
                "CANCELLED_BY_RIDER",
                "CANCELLED_BY_DRIVER",
            ]
        )
    ].copy()

    for _, trip in cancelled_trips.iterrows():

        # Only some cancelled trips have payment attempts.
        if random.random() < 0.30:

            payment_timestamp = pd.to_datetime(
                trip["cancelled_at"]
            )

            payment_status = random.choice(
                [
                    "FAILED",
                    "REFUNDED",
                ]
            )

            payment = generate_payment(
                trip=trip,
                payment_status=payment_status,
                payment_method=random.choice(
                    PAYMENT_METHODS
                ),
                payment_timestamp=payment_timestamp,
            )

            rows.append(payment)

    # ---------------------------------------------------------
    # NO_DRIVER_FOUND
    # ---------------------------------------------------------

    no_driver_trips = trips[
        trips["trip_status"] == "NO_DRIVER_FOUND"
    ].copy()

    for _, trip in no_driver_trips.iterrows():

        # Small number of failed payment attempts.
        if random.random() < 0.05:

            payment_timestamp = pd.to_datetime(
                trip["cancelled_at"]
            )

            payment = generate_payment(
                trip=trip,
                payment_status="FAILED",
                payment_method=random.choice(
                    PAYMENT_METHODS
                ),
                payment_timestamp=payment_timestamp,
            )

            rows.append(payment)

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

    df = generate_payments(
        trips
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR
        / f"payments_{timestamp}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"Generated {len(df):,} payments"
    )

    print(
        f"Trips with payments: "
        f"{df['trip_id'].nunique():,}"
    )

    print(
        f"Unique payment IDs: "
        f"{df['payment_id'].nunique():,}"
    )

    print("\nPayment status distribution:")

    print(
        df["payment_status"].value_counts()
    )

    print("\nPayment method distribution:")

    print(
        df["payment_method"].value_counts()
    )

    print(
        f"\nFile: {output_file}"
    )


if __name__ == "__main__":
    main()