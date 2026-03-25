-- ============================================
-- 01_staging_create_tables.sql
-- Layer: STAGING
-- Purpose:
--   Create staging tables derived from raw.*
--   This layer stores trusted, analytics-ready versions of the raw tables. 
--	 Initial staging tables largely preseve the raw structure, with light standardization added later where needed.
-- ============================================

CREATE SCHEMA IF NOT EXISTS staging;

-- ---------- staging.plan_catalog ----------
DROP TABLE IF EXISTS staging.plan_catalog;

CREATE TABLE staging.plan_catalog (
    	plan_id                 		INTEGER PRIMARY KEY,
    	plan_key                		TEXT,
    	plan_name               		TEXT,
    	plan_rank               		INTEGER,
    	base_monthly_price      		NUMERIC(10,2),
    	location_add_on_price   		NUMERIC(10,2),
    	is_active               		BOOLEAN
);


-- ---------- staging.customers ----------
DROP TABLE IF EXISTS staging.customers;

CREATE TABLE staging.customers (
	customer_id				TEXT PRIMARY KEY,
	segment					TEXT,
	signup_date				DATE,
	initial_plan_key			TEXT,
	initial_contract_type			TEXT,
	initial_locations			INTEGER,
	status					TEXT
);

-- ---------- staging.subscriptions ----------
DROP TABLE IF EXISTS staging.subscriptions;

CREATE TABLE staging.subscriptions (
	subscription_id				TEXT PRIMARY KEY,
	customer_id				TEXT,
	plan_id					INTEGER,
	plan_key				TEXT,
	contract_type				TEXT,
	start_date				DATE,
	end_date				DATE,
	locations				INTEGER,
	discount_pct				NUMERIC(4,2),
	list_mrr				NUMERIC(10,2),
	billed_mrr				NUMERIC(10,2),
	is_active				BOOLEAN
);

-- ---------- staging.subscription_events ----------
DROP TABLE IF EXISTS staging.subscription_events;

CREATE TABLE staging.subscription_events (
    	event_id            			TEXT PRIMARY KEY,
    	customer_id         			TEXT,
    	subscription_id     			TEXT,
    	event_date          			DATE,
    	event_type          			TEXT,
    	old_plan_id         			INTEGER,
    	new_plan_id         			INTEGER,
    	old_locations       			INTEGER,
    	new_locations       			INTEGER,
    	old_discount_pct    			NUMERIC(4,2),
    	new_discount_pct   		 	NUMERIC(4,2)
);

-- ---------- staging.customer_month ----------
DROP TABLE IF EXISTS staging.customer_month;

CREATE TABLE staging.customer_month (
	month_start				DATE NOT NULL,
	customer_id				TEXT NOT NULL,
	plan_id					INTEGER,
	contract_type				TEXT,
	locations				INTEGER,
	list_mrr				NUMERIC(10,2),
	discount_pct				NUMERIC(4,2),
	billed_mrr				NUMERIC(10,2),
	prev_billed_mrr				NUMERIC(10,2),
	mrr_change				NUMERIC(10,2),
	movement_type				TEXT,
	is_active				BOOLEAN NOT NULL,
	PRIMARY KEY (customer_id, month_start)
);