-- ============================================
-- 02_staging_load_from_raw.sql
-- Layer: STAGING
-- Purpose:
--   Load staging tables from raw tables with minimal cleaning.
-- ============================================

-- ---------- staging.plan_catalog (straigth copy) ----------
TRUNCATE TABLE staging.plan_catalog;
INSERT INTO staging.plan_catalog (plan_id, plan_key, plan_name, plan_rank, base_monthly_price, location_add_on_price, is_active)
SELECT plan_id, plan_key, plan_name, plan_rank, base_monthly_price, location_add_on_price, is_active
FROM raw.plan_catalog;

-- ---------- staging.customers (mostly straigth copy) ----------
TRUNCATE TABLE staging.customers;
INSERT INTO staging.customers (customer_id, segment, signup_date, initial_plan_key, initial_contract_type, initial_locations, status)
SELECT customer_id, segment, signup_date, initial_plan_key, initial_contract_type, initial_locations, status
FROM raw.customers;

-- ---------- staging.subscriptions (mostly straigth copy) ----------
TRUNCATE TABLE staging.subscriptions;
INSERT INTO staging.subscriptions (subscription_id, customer_id, plan_id, plan_key, contract_type, start_date, end_date, locations, discount_pct, list_mrr, billed_mrr, is_active)
SELECT subscription_id, customer_id, plan_id, plan_key, contract_type, start_date, end_date, locations, discount_pct, list_mrr, billed_mrr, is_active
FROM raw.subscriptions;

-- ---------- staging.subscription_events (mostly straigth copy) ----------
TRUNCATE TABLE staging.subscription_events;
INSERT INTO staging.subscription_events (event_id, customer_id, subscription_id, event_date, event_type, old_plan_id, new_plan_id, old_locations, new_locations, old_discount_pct, new_discount_pct)
SELECT event_id, customer_id, subscription_id, event_date, event_type, old_plan_id, new_plan_id, old_locations, new_locations, old_discount_pct, new_discount_pct
FROM raw.subscription_events;

-- ---------- staging.customer_month (straight copy) ----------
