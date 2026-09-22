from pathlib import Path
from datetime import datetime, date
import random
import uuid

import pandas as pd
from faker import Faker


fake = Faker("en_IN")

OUTPUT_DIR = Path("data/vehicles")
RECORD_COUNT = 300


VEHICLE_TYPES = [
    "HATCHBACK",
    "SEDAN",
    "SUV",
    "PREMIUM",
    "XL",
]

VEHICLE_MAKES = {
    "HATCHBACK": ["Maruti", "Hyundai", "Tata"],
    "SEDAN": ["Honda", "Hyundai", "Toyota"],
    "SUV": ["Tata", "Mahindra", "Hyundai"],
    "PREMIUM": ["Toyota", "Honda", "Skoda"],
    "XL": ["Toyota", "Mahindra", "Kia"],
}

VEHICLE_MODELS = {
    "Maruti": ["Swift", "Baleno", "WagonR"],
    "Hyundai": ["i20", "Verna", "Creta"],
    "Tata": ["Nexon", "Punch", "Harrier"],
    "Honda": ["City", "Amaze"],
    "Toyota": ["Camry", "Innova"],
    "Mahindra": ["XUV700", "Scorpio"],
    "Skoda": ["Slavia", "Kushaq"],
    "Kia": ["Carens", "Seltos"],
}

FUEL_TYPES = [
    "PETROL",
    "DIESEL",
    "CNG",
    "ELECTRIC",
]

COLORS = [
    "WHITE",
    "BLACK",
    "SILVER",
    "GREY",
    "BLUE",
    "RED",
]

VEHICLE_STATUSES = [
    "ACTIVE",
    "INACTIVE",
    "MAINTENANCE",
    "RETIRED",
]


def generate_vehicles(count: int) -> pd.DataFrame:
    rows = []

    start_date = date(2020, 1, 1)

    for _ in range(count):

        vehicle_id = f"V{uuid.uuid4().hex[:10].upper()}"

        vehicle_type = random.choice(VEHICLE_TYPES)

        make = random.choice(VEHICLE_MAKES[vehicle_type])

        model = random.choice(VEHICLE_MODELS[make])

        vehicle_year = random.randint(2019, 2026)

        registration_date = fake.date_between(
            start_date=start_date,
            end_date=date.today(),
        )

        created_at = datetime.combine(
            registration_date,
            datetime.min.time(),
        )

        updated_at = created_at

        rows.append(
            {
                "vehicle_id": vehicle_id,
                "registration_number": (
                    f"DL{random.randint(10, 99)}"
                    f"{fake.random_letter().upper()}"
                    f"{fake.random_letter().upper()}"
                    f"{random.randint(1000, 9999)}"
                ),
                "vehicle_type": vehicle_type,
                "vehicle_make": make,
                "vehicle_model": model,
                "vehicle_year": vehicle_year,
                "fuel_type": random.choice(FUEL_TYPES),
                "color": random.choice(COLORS),
                "registration_date": registration_date,
                "vehicle_status": random.choices(
                    VEHICLE_STATUSES,
                    weights=[80, 8, 8, 4],
                )[0],
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

    return pd.DataFrame(rows)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_vehicles(RECORD_COUNT)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = (
        OUTPUT_DIR / f"vehicles_{timestamp}.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df):,} vehicles")
    print(f"File: {output_file}")


if __name__ == "__main__":
    main()