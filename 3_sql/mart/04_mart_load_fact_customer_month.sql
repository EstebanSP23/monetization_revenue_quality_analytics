-- ============================================
-- 04_load_fact_customer_month.sql
-- Layer: MART
-- Purpose:
-- 	Load the core monthly fact table from staging.customer_month.
-- ============================================
TRUNCATE TABLE mart.fact_customer_month;
INSERT INTO mart.fact_customer_month (month_start, customer_id, plan_id, contract_type, locations, list_mrr, discount_pct, billed_mrr, prev_billed_mrr, mrr_change, movement_type, is_active)
SELECT month_start, customer_id, plan_id, contract_type, locations, list_mrr, discount_pct, billed_mrr, prev_billed_mrr, mrr_change, movement_type, is_active
FROM staging.customer_month;