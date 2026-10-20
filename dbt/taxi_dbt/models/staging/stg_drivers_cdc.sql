{{ config(
    materialized='view'
) }}

WITH driver_versions AS (

    SELECT *
    FROM {{ ref('stg_drivers') }}

),

versioned AS (

    SELECT
        *,

        LAG(record_hash) OVER (
            PARTITION BY driver_id
            ORDER BY
                updated_at,
                ingested_at,
                source_row_number
        ) AS previous_record_hash,

        LAG(updated_at) OVER (
            PARTITION BY driver_id
            ORDER BY
                updated_at,
                ingested_at,
                source_row_number
        ) AS previous_updated_at

    FROM driver_versions

),

classified AS (

    SELECT
        *,

        CASE
            WHEN previous_record_hash IS NULL
                THEN 'INSERT'

            WHEN record_hash <> previous_record_hash
                THEN 'UPDATE'

            ELSE 'UNCHANGED'

        END AS change_type

    FROM versioned

)

SELECT *
FROM classified