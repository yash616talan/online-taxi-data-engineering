USE DATABASE TAXI_DW;
USE SCHEMA RAW;

CREATE PIPE IF NOT EXISTS RIDERS_PIPE
    AUTO_INGEST = TRUE
    AS
    COPY INTO RIDERS_RAW (
        RIDER_ID,
        FIRST_NAME,
        LAST_NAME,
        EMAIL,
        PHONE_NUMBER,
        DATE_OF_BIRTH,
        GENDER,
        SIGNUP_DATE,
        HOME_LOCATION_ID,
        RIDER_STATUS,
        CREATED_AT,
        UPDATED_AT,
        RAW_RECORD_ID,
        SOURCE_FILE_NAME,
        SOURCE_FILE_PATH,
        SOURCE_ROW_NUMBER,
        BATCH_ID,
        INGESTED_AT,
        LOAD_DATE,
        RECORD_HASH
    )
    FROM (
        SELECT
            $1::VARCHAR,
            $2::VARCHAR,
            $3::VARCHAR,
            $4::VARCHAR,
            $5::VARCHAR,
            $6::DATE,
            $7::VARCHAR,
            $8::TIMESTAMP_NTZ,
            $9::VARCHAR,
            $10::VARCHAR,
            $11::TIMESTAMP_NTZ,
            $12::TIMESTAMP_NTZ,

            SHA2(
                METADATA$FILENAME || ':' || METADATA$FILE_ROW_NUMBER,
                256
            ),

            METADATA$FILENAME,
            METADATA$FILENAME,
            METADATA$FILE_ROW_NUMBER,

            'BATCH_' || REGEXP_SUBSTR(
                METADATA$FILENAME,
                '[0-9]{8}_[0-9]{6}'
            ),

            CURRENT_TIMESTAMP(),
            CURRENT_DATE(),

            SHA2(
                ARRAY_TO_STRING(
                    ARRAY_CONSTRUCT(
                        $1, $2, $3, $4, $5, $6,
                        $7, $8, $9, $10, $11, $12
                    ),
                    '|'
                ),
                256
            )

        FROM @TAXI_S3_STAGE/riders/
    )
    FILE_FORMAT = (
        FORMAT_NAME = 'TAXI_DW.RAW.TAXI_CSV_FORMAT'
    );