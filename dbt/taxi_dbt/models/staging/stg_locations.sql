{{ config(
    materialized='view'
) }}

WITH source_data AS (

    SELECT
        location_id,
        city,
        state,
        country,
        postal_code,
        latitude,
        longitude,
        zone_name,
        location_type,
        created_at,
        updated_at,

        source_file_name,
        source_file_path,
        source_row_number,
        batch_id,
        ingested_at,
        load_date

    FROM {{ source('raw', 'locations_raw') }}

),

standardized AS (

    SELECT
        TRIM(location_id) AS location_id,

        TRIM(city) AS city,
        TRIM(state) AS state,
        TRIM(country) AS country,
        TRIM(postal_code) AS postal_code,

        CAST(latitude AS NUMBER(10,6)) AS latitude,
        CAST(longitude AS NUMBER(10,6)) AS longitude,

        TRIM(zone_name) AS zone_name,
        UPPER(TRIM(location_type)) AS location_type,

        CAST(created_at AS TIMESTAMP_NTZ) AS created_at,
        CAST(updated_at AS TIMESTAMP_NTZ) AS updated_at,

        source_file_name,
        source_file_path,
        source_row_number,
        batch_id,
        ingested_at,
        load_date

    FROM source_data

),

deduplicated AS (

    SELECT *

    FROM standardized

    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY location_id
        ORDER BY
            updated_at DESC,
            ingested_at DESC,
            source_row_number DESC
    ) = 1

)

SELECT *
FROM deduplicated