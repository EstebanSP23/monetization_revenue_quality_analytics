-- ============================================
-- 01_raw_create_tables.sql
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
    plan_id                 		INTEGER PRIMARY KEY,
    plan_key                		TEXT,
    plan_name               		TEXT,
    plan_rank               		INTEGER,
    base_monthly_price      		NUMERIC(10,2),
    location_add_on_price   		NUMERIC(10,2),
    is_active               		BOOLEAN
);

-- ============================================
-- raw.customers
-- 1 row per customer
-- ============================================

DROP TABLE IF EXISTS raw.customers;

CREATE TABLE raw.customers (
	customer_id			TEXT PRIMARY KEY,
	segment				TEXT,
	signup_date			DATE,
	initial_plan_key		TEXT,
	initial_contract_type		TEXT,
	initial_locations		INTEGER,
	status				TEXT
);

-- ============================================
-- raw.subscriptions
-- 1 row per subscription state period 
-- ============================================

DROP TABLE IF EXISTS raw.subscriptions;

CREATE TABLE raw.subscriptions (
	subscription_id			TEXT PRIMARY KEY,
	customer_id			TEXT,
	plan_id				INTEGER,
	plan_key			TEXT,
	contract_type			TEXT,
	start_date			DATE,
	end_date			DATE,
	locations			INTEGER,
	discount_pct			NUMERIC(4,2),
	list_mrr			NUMERIC(10,2),
	billed_mrr			NUMERIC(10,2),
	is_active			BOOLEAN
);

-- ============================================
-- raw.subscription_events
-- 1 row per subscription event
-- ============================================

DROP TABLE IF EXISTS raw.subscription_events;

CREATE TABLE raw.subscription_events (
    event_id            		TEXT PRIMARY KEY,
    customer_id         		TEXT,
    subscription_id     		TEXT,
    event_date          		DATE,
    event_type          		TEXT,
    old_plan_id         		INTEGER,
    new_plan_id         		INTEGER,
    old_locations       		INTEGER,
    new_locations       		INTEGER,
    old_discount_pct    		NUMERIC(4,2),
    new_discount_pct   		 	NUMERIC(4,2)
);

-- ============================================
-- raw.customer_month
-- 1 row per customer per month
-- ============================================

DROP TABLE IF EXISTS raw.customer_month;

CREATE TABLE raw.customer_month (
	month_start			DATE,
	customer_id			TEXT,
	plan_id				INTEGER,
	contract_type			TEXT,
	locations			INTEGER,
	list_mrr			NUMERIC(10,2),
	discount_pct			NUMERIC(4,2),
	billed_mrr			NUMERIC(10,2),
	prev_billed_mrr			NUMERIC(10,2),
	mrr_change			NUMERIC(10,2),
	movement_type			TEXT,
	is_active			BOOLEAN
);