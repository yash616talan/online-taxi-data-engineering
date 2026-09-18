USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS LOCATIONS_RAW (

    location_id VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    postal_code VARCHAR,
    latitude NUMBER(10,6),
    longitude NUMBER(10,6),
    zone_name VARCHAR,
    location_type VARCHAR,
    created_at TIMESTAMP_NTZ,
    updated_at TIMESTAMP_NTZ,

    raw_record_id VARCHAR,
    source_file_name VARCHAR,
    source_file_path VARCHAR,
    source_row_number NUMBER(38,0),
    batch_id VARCHAR,
    ingested_at TIMESTAMP_NTZ,
    load_date DATE,
    record_hash VARCHAR
);