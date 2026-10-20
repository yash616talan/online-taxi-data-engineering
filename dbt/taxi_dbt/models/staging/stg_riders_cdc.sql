{{ config(
    materialized='view'
) }}

WITH rider_versions AS (

    SELECT
        *
    FROM {{ ref('stg_riders') }}

),

versioned AS (

    SELECT
        *,

        LAG(record_hash) OVER (
            PARTITION BY rider_id
            ORDER BY
                updated_at,
                ingested_at,
                source_row_number
        ) AS previous_record_hash,

        LAG(updated_at) OVER (
            PARTITION BY rider_id
            ORDER BY
                updated_at,
                ingested_at,
                source_row_number
        ) AS previous_updated_at

    FROM rider_versions

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