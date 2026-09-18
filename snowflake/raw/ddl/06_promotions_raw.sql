USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS PROMOTIONS_RAW (

    promotion_id VARCHAR,
    promotion_code VARCHAR,
    promotion_name VARCHAR,
    promotion_type VARCHAR,
    discount_value NUMBER(18,2),
    max_discount_amount NUMBER(18,2),
    min_trip_amount NUMBER(18,2),
    start_at TIMESTAMP_NTZ,
    end_at TIMESTAMP_NTZ,
    usage_limit NUMBER(38,0),
    promotion_status VARCHAR,
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