{{ config(
    materialized='view'
) }}

WITH source_data AS (

    SELECT
        driver_id,
        first_name,
        last_name,
        email,
        phone_number,
        license_number,
        license_expiry_date,
        joining_date,
        home_location_id,
        driver_status,
        driver_tier,
        created_at,
        updated_at,

        source_file_name,
        source_file_path,
        source_row_number,
        batch_id,
        ingested_at,
        load_date

    FROM {{ source('raw', 'drivers_raw') }}

),

standardized AS (

    SELECT
        TRIM(driver_id) AS driver_id,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        LOWER(TRIM(email)) AS email,
        TRIM(phone_number) AS phone_number,
        TRIM(license_number) AS license_number,

        CAST(
            license_expiry_date AS DATE
        ) AS license_expiry_date,

        CAST(
            joining_date AS DATE
        ) AS joining_date,

        TRIM(home_location_id) AS home_location_id,

        UPPER(TRIM(driver_status)) AS driver_status,
        UPPER(TRIM(driver_tier)) AS driver_tier,

        CAST(
            created_at AS TIMESTAMP_NTZ
        ) AS created_at,

        CAST(
            updated_at AS TIMESTAMP_NTZ
        ) AS updated_at,

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
                COALESCE(license_number, ''),
                COALESCE(
                    TO_VARCHAR(license_expiry_date),
                    ''
                ),
                COALESCE(
                    TO_VARCHAR(joining_date),
                    ''
                ),
                COALESCE(home_location_id, ''),
                COALESCE(driver_status, ''),
                COALESCE(driver_tier, '')
            ),
            256
        ) AS record_hash

    FROM standardized

)

SELECT *
FROM hashed