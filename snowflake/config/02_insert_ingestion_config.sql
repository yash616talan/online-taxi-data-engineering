USE DATABASE TAXI_DW;
USE SCHEMA INGESTION_CONFIG;

INSERT INTO INGESTION_CONFIG (
    entity_name,
    source_path,
    target_table,
    load_type,
    watermark_column,
    is_active,
    created_at,
    updated_at
)
VALUES
    ('RIDER', 'riders/', 'RAW.RIDERS_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('DRIVER', 'drivers/', 'RAW.DRIVERS_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('VEHICLE', 'vehicles/', 'RAW.VEHICLES_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('DRIVER_VEHICLE_ASSIGNMENT', 'driver_vehicle_assignments/', 'RAW.DRIVER_VEHICLE_ASSIGNMENTS_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('LOCATION', 'locations/', 'RAW.LOCATIONS_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('PROMOTION', 'promotions/', 'RAW.PROMOTIONS_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('TRIP', 'trips/', 'RAW.TRIPS_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('TRIP_EVENT', 'trip_events/', 'RAW.TRIP_EVENTS_RAW', 'APPEND', NULL, TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('PAYMENT', 'payments/', 'RAW.PAYMENTS_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('RATING', 'ratings/', 'RAW.RATINGS_RAW', 'APPEND', NULL, TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
    ('DRIVER_EARNING', 'driver_earnings/', 'RAW.DRIVER_EARNINGS_RAW', 'MERGE', 'updated_at', TRUE, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());