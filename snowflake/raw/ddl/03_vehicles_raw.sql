USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS VEHICLES_RAW (

    vehicle_id VARCHAR,
    registration_number VARCHAR,
    vehicle_type VARCHAR,
    vehicle_make VARCHAR,
    vehicle_model VARCHAR,
    vehicle_year NUMBER(38,0),
    fuel_type VARCHAR,
    color VARCHAR,
    registration_date DATE,
    vehicle_status VARCHAR,
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