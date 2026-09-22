from pathlib import Path
from datetime import datetime
import random
import uuid

import pandas as pd
from faker import Faker


fake = Faker("en_IN")

OUTPUT_DIR = Path("data/locations")
RECORD_COUNT = 200


CITIES = [
    ("Mumbai", "Maharashtra", "India"),
    ("Delhi", "Delhi", "India"),
    ("Bengaluru", "Karnataka", "India"),
    ("Hyderabad", "Telangana", "India"),
    ("Pune", "Maharashtra", "India"),
    ("Chennai", "Tamil Nadu", "India"),
    ("Kolkata", "West Bengal", "India"),
    ("Ahmedabad", "Gujarat", "India"),
    ("Jaipur", "Rajasthan", "India"),
    ("Agra", "Uttar Pradesh", "India"),
]

LOCATION_TYPES = [
    "AIRPORT",
    "RESIDENTIAL",
    "COMMERCIAL",
    "BUSINESS_DISTRICT",
    "RAILWAY_STATION",
    "HOTEL",
    "UNIVERSITY",
    "OTHER",
]


def generate_locations(count: int) -> pd.DataFrame:
    rows = []

    for _ in range(count):
        city, state, country = random.choice(CITIES)

        created_at = datetime.now()
        updated_at = created_at

        rows.append(
            {
                "location_id": f"L{uuid.uuid4().hex[:10].upper()}",
                "city": city,
                "state": state,
                "country": country,
                "postal_code": fake.postcode(),
                "latitude": round(
                    random.uniform(8.0, 28.0), 6
                ),
                "longitude": round(
                    random.uniform(68.0, 88.0), 6
                ),
                "zone_name": f"{city}_ZONE_{random.randint(1, 10)}",
                "location_type": random.choice(LOCATION_TYPES),
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

    return pd.DataFrame(rows)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_locations(RECORD_COUNT)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"locations_{timestamp}.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df):,} locations")
    print(f"File: {output_file}")


if __name__ == "__main__":
    main()