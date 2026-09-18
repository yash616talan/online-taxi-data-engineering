USE DATABASE TAXI_DW;

CREATE STORAGE INTEGRATION TAXI_S3_INTEGRATION
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = 'S3'
    ENABLED = TRUE
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::749794722927:role/online-taxi-data-snowflake-role'
    STORAGE_ALLOWED_LOCATIONS = (
        's3://online-taxi-data-yash/'
    );