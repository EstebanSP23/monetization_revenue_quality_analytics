-- ============================================
-- 01_mart_create_dimensions.sql
-- Layer: MART
-- Purpose:
--   Create dimension tables that provide descriptive context for MART fact tables and downstream analytics.
-- ============================================

CREATE SCHEMA IF NOT EXISTS mart;

-- ---------- mart.dim_date ----------
DROP TABLE IF EXISTS mart.dim_date;
CREATE TABLE mart.dim_date (
	month_start				DATE PRIMARY KEY,
	year					INTEGER,
	month_num				INTEGER,
	year_month				TEXT,
	quarter					INTEGER,
	year_quarter			TEXT
);

-- ---------- mart.dim_plan ----------
DROP TABLE IF EXISTS mart.dim_plan;
CREATE TABLE mart.dim_plan (
	plan_id					INTEGER PRIMARY KEY,
	plan_key				TEXT,
	plan_name				TEXT,
	plan_rank				INTEGER,
	base_monthly_price		NUMERIC(10,2),
	location_add_on_price	NUMERIC(10,2),
	is_active				BOOLEAN
);

-- ---------- mart.dim_customer ----------
DROP TABLE IF EXISTS mart.dim_customer;
CREATE TABLE mart.dim_customer (
	customer_id				TEXT PRIMARY KEY,
	segment					TEXT,
	signup_date				DATE,
	initial_plan_key		TEXT,
	initial_contract_type	TEXT,
	initial_locations		INTEGER,
	status					TEXT,
	signup_month			DATE
);