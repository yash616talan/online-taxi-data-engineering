USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS TRIPS_RAW (

    trip_id VARCHAR,
    rider_id VARCHAR,
    driver_id VARCHAR,
    vehicle_id VARCHAR,
    pickup_location_id VARCHAR,
    dropoff_location_id VARCHAR,
    promotion_id VARCHAR,
    trip_status VARCHAR,

    requested_at TIMESTAMP_NTZ,
    accepted_at TIMESTAMP_NTZ,
    driver_arrived_at TIMESTAMP_NTZ,
    started_at TIMESTAMP_NTZ,
    completed_at TIMESTAMP_NTZ,
    cancelled_at TIMESTAMP_NTZ,

    cancellation_reason VARCHAR,

    distance_km NUMBER(12,3),
    duration_minutes NUMBER(10,2),

    base_fare NUMBER(18,2),
    surge_amount NUMBER(18,2),
    discount_amount NUMBER(18,2),
    tax_amount NUMBER(18,2),
    total_fare NUMBER(18,2),

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