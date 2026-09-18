USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS PAYMENTS_RAW (

    payment_id VARCHAR,
    trip_id VARCHAR,
    rider_id VARCHAR,
    payment_method VARCHAR,
    payment_status VARCHAR,
    transaction_reference VARCHAR,
    amount NUMBER(18,2),
    currency VARCHAR,
    payment_initiated_at TIMESTAMP_NTZ,
    payment_completed_at TIMESTAMP_NTZ,
    failure_reason VARCHAR,
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