USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS RATINGS_RAW (

    rating_id VARCHAR,
    trip_id VARCHAR,
    rater_type VARCHAR,
    rater_id VARCHAR,
    rated_entity_type VARCHAR,
    rated_entity_id VARCHAR,
    rating_value NUMBER(3,2),
    rating_comment VARCHAR,
    rating_timestamp TIMESTAMP_NTZ,
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