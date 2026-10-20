from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RIDER_DIR = DATA_DIR / "riders"
DRIVER_DIR = DATA_DIR / "drivers"
LOCATION_DIR = DATA_DIR / "locations"


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
POPULATED_RATIO = 0.95
RANDOM_SEED = 42

# IMPORTANT:
# These are the clean original source files.
# Do NOT use the latest generated update files as input.
RIDER_SOURCE_FILE = "riders_20260918_105528.csv"
DRIVER_SOURCE_FILE = "drivers_20260921_092637.csv"
LOCATION_SOURCE_FILE = "locations_20260921_094525.csv"


# ---------------------------------------------------------
# Helper: get specific source CSV
# ---------------------------------------------------------
def get_source_csv(directory: Path, filename: str) -> Path:
    file_path = directory / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    return file_path


# ---------------------------------------------------------
# Load source files
# ---------------------------------------------------------
def load_source_data():
    # -----------------------------------------------------
    # IMPORTANT:
    # Always read from the original clean source files.
    #
    # We intentionally DO NOT use "latest CSV" logic here.
    # Otherwise a previously generated update batch could
    # become the source for the next update.
    # -----------------------------------------------------
    rider_file = get_source_csv(
        RIDER_DIR,
        RIDER_SOURCE_FILE
    )

    driver_file = get_source_csv(
        DRIVER_DIR,
        DRIVER_SOURCE_FILE
    )

    location_file = get_source_csv(
        LOCATION_DIR,
        LOCATION_SOURCE_FILE
    )

    # -----------------------------------------------------
    # Read Riders
    # -----------------------------------------------------
    riders = pd.read_csv(
        rider_file,
        dtype={
            "rider_id": "string",
            "phone_number": "string"
        }
    )

    # -----------------------------------------------------
    # Read Drivers
    # -----------------------------------------------------
    drivers = pd.read_csv(
        driver_file,
        dtype={
            "driver_id": "string",
            "phone_number": "string"
        }
    )

    # -----------------------------------------------------
    # Read Locations
    # -----------------------------------------------------
    locations = pd.read_csv(
        location_file,
        dtype={
            "location_id": "string"
        }
    )

    print("\nSource files:")
    print(f"  Rider source   : {rider_file.name}")
    print(f"  Driver source  : {driver_file.name}")
    print(f"  Location source: {location_file.name}")

    return riders, drivers, locations


# ---------------------------------------------------------
# Validate phone numbers
# ---------------------------------------------------------
def validate_phone_numbers(
    original_df: pd.DataFrame,
    entity_name: str
):
    if "phone_number" not in original_df.columns:
        raise ValueError(
            f"{entity_name}: phone_number column not found."
        )

    phone_values = (
        original_df["phone_number"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    # Phone numbers should remain strings.
    # This validation specifically protects against
    # accidental conversion to numeric values.
    invalid_lengths = phone_values[
        ~phone_values.str.len().isin([10])
    ]

    if not invalid_lengths.empty:
        print(
            f"\nWARNING: {entity_name} contains "
            f"{len(invalid_lengths)} phone numbers "
            f"that are not 10 characters long."
        )

    # Check that no values look like floating-point numbers.
    numeric_like = phone_values[
        phone_values.str.match(r"^\d+\.0$")
    ]

    if not numeric_like.empty:
        raise ValueError(
            f"{entity_name}: phone numbers appear to have "
            f"been converted to numeric values."
        )


# ---------------------------------------------------------
# Apply location updates
# ---------------------------------------------------------
def update_home_locations(
    df: pd.DataFrame,
    location_ids,
    entity_name: str
):
    df = df.copy()

    total_records = len(df)

    populated_count = int(
        total_records * POPULATED_RATIO
    )

    null_count = (
        total_records - populated_count
    )

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    # -----------------------------------------------------
    # Randomly select records that receive a location
    # -----------------------------------------------------
    populated_indices = rng.choice(
        df.index,
        size=populated_count,
        replace=False
    )

    # -----------------------------------------------------
    # Initially set every home_location_id to NULL
    # -----------------------------------------------------
    df["home_location_id"] = pd.NA

    # -----------------------------------------------------
    # Assign valid location IDs to 95% of records
    # -----------------------------------------------------
    df.loc[
        populated_indices,
        "home_location_id"
    ] = rng.choice(
        location_ids,
        size=populated_count,
        replace=True
    )

    # -----------------------------------------------------
    # Update updated_at
    # -----------------------------------------------------
    update_timestamp = datetime.now()

    df["updated_at"] = update_timestamp

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------
    actual_populated = (
        df["home_location_id"]
        .notna()
        .sum()
    )

    actual_null = (
        df["home_location_id"]
        .isna()
        .sum()
    )

    expected_populated = populated_count
    expected_null = null_count

    assert actual_populated == expected_populated, (
        f"{entity_name}: expected "
        f"{expected_populated} populated locations "
        f"but got {actual_populated}"
    )

    assert actual_null == expected_null, (
        f"{entity_name}: expected "
        f"{expected_null} NULL locations "
        f"but got {actual_null}"
    )

    print(
        f"\n{entity_name} update validation:"
    )

    print(
        f"  Total records       : "
        f"{total_records}"
    )

    print(
        f"  Populated locations : "
        f"{actual_populated}"
    )

    print(
        f"  NULL locations      : "
        f"{actual_null}"
    )

    return df


# ---------------------------------------------------------
# Validate that protected columns did not change
# ---------------------------------------------------------
def validate_preserved_columns(
    original_df: pd.DataFrame,
    updated_df: pd.DataFrame,
    id_column: str,
    entity_name: str
):
    # -----------------------------------------------------
    # Required columns that should NOT change during this
    # controlled home_location update.
    # -----------------------------------------------------
    protected_columns = [
        id_column,
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "date_of_birth",
        "gender",
        "signup_date",
        "rider_status"
        if entity_name == "RIDER"
        else "driver_status",
        "created_at"
    ]

    for column in protected_columns:

        if column not in original_df.columns:
            continue

        if column not in updated_df.columns:
            raise ValueError(
                f"{entity_name}: column '{column}' "
                f"is missing from updated data."
            )

        original_values = (
            original_df[column]
            .astype("string")
            .fillna("<NULL>")
        )

        updated_values = (
            updated_df[column]
            .astype("string")
            .fillna("<NULL>")
        )

        differences = (
            original_values != updated_values
        )

        difference_count = differences.sum()

        if difference_count > 0:
            raise ValueError(
                f"{entity_name}: {difference_count} "
                f"records changed unexpectedly in "
                f"column '{column}'."
            )

    print(
        f"\n{entity_name}: protected columns "
        f"validated successfully."
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():

    # -----------------------------------------------------
    # Load clean original source data
    # -----------------------------------------------------
    riders, drivers, locations = (
        load_source_data()
    )

    # -----------------------------------------------------
    # Validate source phone numbers BEFORE making changes
    # -----------------------------------------------------
    validate_phone_numbers(
        riders,
        "RIDER"
    )

    validate_phone_numbers(
        drivers,
        "DRIVER"
    )

    # -----------------------------------------------------
    # Preserve original IDs
    # -----------------------------------------------------
    original_rider_ids = set(
        riders["rider_id"]
    )

    original_driver_ids = set(
        drivers["driver_id"]
    )

    # -----------------------------------------------------
    # Get valid location IDs
    # -----------------------------------------------------
    location_ids = (
        locations["location_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if not location_ids:
        raise ValueError(
            "No valid location IDs found."
        )

    print(
        f"\nAvailable location IDs: "
        f"{len(location_ids)}"
    )

    # -----------------------------------------------------
    # Create updated Rider version
    # -----------------------------------------------------
    updated_riders = update_home_locations(
        riders,
        location_ids,
        "RIDER"
    )

    # -----------------------------------------------------
    # Create updated Driver version
    # -----------------------------------------------------
    updated_drivers = update_home_locations(
        drivers,
        location_ids,
        "DRIVER"
    )

    # -----------------------------------------------------
    # Validate Rider IDs are unchanged
    # -----------------------------------------------------
    assert set(
        updated_riders["rider_id"]
    ) == original_rider_ids, (
        "Rider IDs changed during update!"
    )

    # -----------------------------------------------------
    # Validate Driver IDs are unchanged
    # -----------------------------------------------------
    assert set(
        updated_drivers["driver_id"]
    ) == original_driver_ids, (
        "Driver IDs changed during update!"
    )

    # -----------------------------------------------------
    # Validate all populated location IDs exist
    # -----------------------------------------------------
    valid_location_ids = set(
        location_ids
    )

    rider_locations = set(
        updated_riders[
            "home_location_id"
        ]
        .dropna()
        .astype(str)
    )

    driver_locations = set(
        updated_drivers[
            "home_location_id"
        ]
        .dropna()
        .astype(str)
    )

    assert rider_locations.issubset(
        valid_location_ids
    ), (
        "Rider contains invalid location IDs!"
    )

    assert driver_locations.issubset(
        valid_location_ids
    ), (
        "Driver contains invalid location IDs!"
    )

    # -----------------------------------------------------
    # Validate that existing business attributes were
    # preserved exactly.
    # -----------------------------------------------------
    validate_preserved_columns(
        riders,
        updated_riders,
        "rider_id",
        "RIDER"
    )

    validate_preserved_columns(
        drivers,
        updated_drivers,
        "driver_id",
        "DRIVER"
    )

    # -----------------------------------------------------
    # Generate timestamped filenames
    # -----------------------------------------------------
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    rider_output = (
        RIDER_DIR /
        f"riders_{timestamp}.csv"
    )

    driver_output = (
        DRIVER_DIR /
        f"drivers_{timestamp}.csv"
    )

    # -----------------------------------------------------
    # Write update batches
    # -----------------------------------------------------
    updated_riders.to_csv(
        rider_output,
        index=False
    )

    updated_drivers.to_csv(
        driver_output,
        index=False
    )

    # -----------------------------------------------------
    # Final validation
    # -----------------------------------------------------
    print(
        "\nUpdate batches generated successfully."
    )

    print(
        f"\nRider update : "
        f"{rider_output}"
    )

    print(
        f"Driver update: "
        f"{driver_output}"
    )

    print("\nFinal validation:")

    print(
        f"  Riders : "
        f"{len(updated_riders)}"
    )

    print(
        f"  Drivers: "
        f"{len(updated_drivers)}"
    )

    # -----------------------------------------------------
    # Verify phone numbers after writing
    # -----------------------------------------------------
    saved_riders = pd.read_csv(
        rider_output,
        dtype={
            "rider_id": "string",
            "phone_number": "string"
        }
    )

    saved_drivers = pd.read_csv(
        driver_output,
        dtype={
            "driver_id": "string",
            "phone_number": "string"
        }
    )

    # -----------------------------------------------------
    # Compare phone numbers against original source
    # -----------------------------------------------------
    original_rider_phone = (
        riders
        .set_index("rider_id")["phone_number"]
        .fillna("<NULL>")
        .astype("string")
    )

    saved_rider_phone = (
        saved_riders
        .set_index("rider_id")["phone_number"]
        .fillna("<NULL>")
        .astype("string")
    )

    rider_phone_diff = (
        original_rider_phone
        != saved_rider_phone
    )

    rider_phone_diff_count = (
        rider_phone_diff.sum()
    )

    assert rider_phone_diff_count == 0, (
        f"Rider phone numbers changed for "
        f"{rider_phone_diff_count} records!"
    )

    original_driver_phone = (
        drivers
        .set_index("driver_id")["phone_number"]
        .fillna("<NULL>")
        .astype("string")
    )

    saved_driver_phone = (
        saved_drivers
        .set_index("driver_id")["phone_number"]
        .fillna("<NULL>")
        .astype("string")
    )

    driver_phone_diff = (
        original_driver_phone
        != saved_driver_phone
    )

    driver_phone_diff_count = (
        driver_phone_diff.sum()
    )

    assert driver_phone_diff_count == 0, (
        f"Driver phone numbers changed for "
        f"{driver_phone_diff_count} records!"
    )

    print(
        "\nPhone number validation:"
    )

    print(
        "  Rider phone numbers : PASS"
    )

    print(
        "  Driver phone numbers: PASS"
    )

    print(
        "\nAll validations passed."
    )


if __name__ == "__main__":
    main()