-- ============================================
-- 03_mart_create_fact_customer_month.sql
-- Layer: MART
-- Purpose:
-- 	Create the core fact table at grain:
-- 		One row per customer per month with the core revenue and monetization 
--		fields needed for trend, retention, and revenue movement analysis.
-- ============================================
DROP TABLE IF EXISTS mart.fact_customer_month CASCADE;
CREATE TABLE mart.fact_customer_month (
	month_start				DATE NOT NULL,
	customer_id				TEXT NOT NULL,
	plan_id					INTEGER,
	contract_type			TEXT,
	locations				INTEGER,
	list_mrr				NUMERIC(10,2),
	discount_pct			NUMERIC(4,2),
	billed_mrr				NUMERIC(10,2),
	prev_billed_mrr			NUMERIC(10,2),
	mrr_change				NUMERIC(10,2),
	movement_type			TEXT,	
	is_active				BOOLEAN NOT NULL,
	PRIMARY KEY (customer_id, month_start)
);