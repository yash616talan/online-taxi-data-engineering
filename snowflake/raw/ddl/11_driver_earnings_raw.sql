USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS DRIVER_EARNINGS_RAW (

    earning_id VARCHAR,
    trip_id VARCHAR,
    driver_id VARCHAR,
    earning_type VARCHAR,

    gross_fare NUMBER(18,2),
    platform_commission NUMBER(18,2),
    driver_base_earning NUMBER(18,2),
    surge_earning NUMBER(18,2),
    incentive_amount NUMBER(18,2),
    adjustment_amount NUMBER(18,2),
    net_driver_earning NUMBER(18,2),

    earning_status VARCHAR,
    earning_timestamp TIMESTAMP_NTZ,
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