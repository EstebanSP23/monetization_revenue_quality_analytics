-- ============================================
-- 01_raw__create_tables.sql
-- Layer: RAW
-- Purpose:
--   Create the RAW tables that store CSV data "as loaded".
--   No business logic here — only structure.
--
-- How to run (pgAdmin Query Tool):
--   1) Connect to database: monetization_revenue_quality_analytics
--   2) Execute this script
-- ============================================

-- Ensure schemas exist (safe to run multiple times)
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS mart;

-- ============================================
-- raw.plan_catalog
-- 1 row per subscription plan
-- ============================================

DROP TABLE IF EXISTS raw.plan_catalog;

CREATE TABLE raw.plan_catalog (
    plan_id                 INTEGER PRIMARY KEY,
    plan_key                TEXT,
    plan_name               TEXT,
    plan_rank               INTEGER,
    base_monthly_price      NUMERIC(10,2),
    location_add_on_price   NUMERIC(10,2),
    is_active               BOOLEAN
);