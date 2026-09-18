USE DATABASE TAXI_DW;
USE SCHEMA INGESTION_AUDIT;

CREATE TABLE IF NOT EXISTS INGESTION_AUDIT (
    batch_id VARCHAR,
    entity_name VARCHAR,
    file_name VARCHAR,
    status VARCHAR,
    records_loaded NUMBER(38,0),
    started_at TIMESTAMP_NTZ,
    completed_at TIMESTAMP_NTZ,
    error_message VARCHAR
);