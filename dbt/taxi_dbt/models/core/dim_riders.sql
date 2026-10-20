{{ config(
    materialized='table'
) }}

WITH rider_changes AS (

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

        record_hash,

        source_file_name,
        source_file_path,
        source_row_number,
        batch_id,
        ingested_at,
        load_date,

        change_type

    FROM {{ ref('stg_riders_cdc') }}

    WHERE change_type IN ('INSERT', 'UPDATE')

),

versioned AS (

    SELECT
        *,

        LEAD(updated_at) OVER (
            PARTITION BY rider_id
            ORDER BY
                updated_at,
                ingested_at,
                source_row_number
        ) AS next_updated_at,

        ROW_NUMBER() OVER (
            PARTITION BY rider_id
            ORDER BY
                updated_at,
                ingested_at,
                source_row_number
        ) AS version_number

    FROM rider_changes

),

final AS (

    SELECT

        SHA2(
            CONCAT_WS(
                '||',
                rider_id,
                TO_VARCHAR(updated_at),
                record_hash
            ),
            256
        ) AS rider_version_key,

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

        updated_at AS valid_from,

        next_updated_at AS valid_to,

        CASE
            WHEN next_updated_at IS NULL
                THEN TRUE
            ELSE FALSE
        END AS is_current,

        version_number,

        record_hash,

        source_file_name,
        source_file_path,
        source_row_number,
        batch_id,
        ingested_at,
        load_date

    FROM versioned

)

SELECT *
FROM final