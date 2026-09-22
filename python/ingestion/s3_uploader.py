import sys
from pathlib import Path

import boto3


BUCKET_NAME = "online-taxi-data-yash"
AWS_PROFILE = "taxi-project"


def upload_file(local_file: str, s3_key: str):
    session = boto3.Session(profile_name=AWS_PROFILE)
    s3 = session.client("s3")

    s3.upload_file(
        local_file,
        BUCKET_NAME,
        s3_key,
    )

    print(f"Uploaded: {local_file}")
    print(f"S3: s3://{BUCKET_NAME}/{s3_key}")


def main():
    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python python/ingestion/s3_uploader.py <entity>"
        )

    entity = sys.argv[1].lower()

    data_dir = Path("data") / entity

    if not data_dir.exists():
        raise FileNotFoundError(
            f"Data directory does not exist: {data_dir}"
        )

    csv_files = sorted(data_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {data_dir}"
        )

    csv_file = csv_files[-1]

    s3_key = f"{entity}/{csv_file.name}"

    upload_file(
        str(csv_file),
        s3_key,
    )


if __name__ == "__main__":
    main()