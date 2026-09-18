USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS TRIP_EVENTS_RAW (

    event_id VARCHAR,
    trip_id VARCHAR,
    event_type VARCHAR,
    event_timestamp TIMESTAMP_NTZ,
    event_sequence NUMBER(38,0),
    driver_id VARCHAR,
    vehicle_id VARCHAR,
    location_id VARCHAR,
    event_source VARCHAR,
    created_at TIMESTAMP_NTZ,

    raw_record_id VARCHAR,
    source_file_name VARCHAR,
    source_file_path VARCHAR,
    source_row_number NUMBER(38,0),
    batch_id VARCHAR,
    ingested_at TIMESTAMP_NTZ,
    load_date DATE,
    record_hash VARCHAR
);