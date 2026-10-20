{{ config(
    materialized='view'
) }}

WITH source_data AS (

    SELECT
        rider_id,
        first_name,
        last_name,
        email,
        phone_number,
        date_of_birth,
        gender,
        signup_date,
        home_location_id,
        rider_status,
        created_at,
        updated_at,

        source_file_name,
        source_file_path,
        source_row_number,
        batch_id,
        ingested_at,
        load_date

    FROM {{ source('raw', 'riders_raw') }}

),

standardized AS (

    SELECT
        TRIM(rider_id) AS rider_id,

        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,

        LOWER(TRIM(email)) AS email,
        TRIM(phone_number) AS phone_number,

        CAST(date_of_birth AS DATE) AS date_of_birth,

        UPPER(TRIM(gender)) AS gender,

        CAST(signup_date AS DATE) AS signup_date,

        TRIM(home_location_id) AS home_location_id,

        UPPER(TRIM(rider_status)) AS rider_status,

        CAST(created_at AS TIMESTAMP_NTZ) AS created_at,
        CAST(updated_at AS TIMESTAMP_NTZ) AS updated_at,

        -- Source lineage
        source_file_name,
        source_file_path,
        source_row_number,
        batch_id,
        ingested_at,
        load_date

    FROM source_data

),

hashed AS (

    SELECT
        *,

        SHA2(
            CONCAT_WS(
                '||',
                COALESCE(first_name, ''),
                COALESCE(last_name, ''),
                COALESCE(email, ''),
                COALESCE(phone_number, ''),
                COALESCE(TO_VARCHAR(date_of_birth), ''),
                COALESCE(gender, ''),
                COALESCE(TO_VARCHAR(signup_date), ''),
                COALESCE(home_location_id, ''),
                COALESCE(rider_status, '')
            ),
            256
        ) AS record_hash

    FROM standardized

)

SELECT *
FROM hashed