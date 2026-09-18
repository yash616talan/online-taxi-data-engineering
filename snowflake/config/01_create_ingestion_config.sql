USE DATABASE TAXI_DW;
USE SCHEMA INGESTION_CONFIG;

CREATE TABLE IF NOT EXISTS INGESTION_CONFIG (
    entity_name VARCHAR,
    source_path VARCHAR,
    target_table VARCHAR,
    load_type VARCHAR,
    watermark_column VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP_NTZ,
    updated_at TIMESTAMP_NTZ
);