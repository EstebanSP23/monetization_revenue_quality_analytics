-- ============================================
-- 02_mart_load_dimensions.sql
-- Layer: MART
-- Purpose:
--   Load dimension tables.
-- ============================================

-- ---------- mart.dim_date ----------
TRUNCATE TABLE mart.dim_date;
INSERT INTO mart.dim_date(month_start, year, month_num, year_month, quarter, year_quarter)
WITH month_series AS (
    SELECT generate_series(
        (SELECT MIN(month_start) FROM staging.customer_month),
        (SELECT MAX(month_start) FROM staging.customer_month),
        INTERVAL '1 month'
    )::date AS month_start
)
SELECT
	month_start,
	EXTRACT(YEAR from month_start)::INT			AS year,
	EXTRACT(MONTH from month_start)::INT 			AS month_num,
	TO_CHAR(month_start, 'YYYY-MM')				AS year_month,
	EXTRACT(QUARTER from month_start)::INT			AS quarter,
	TO_CHAR(month_start, 'YYYY-"Q"Q')			AS year_quarter
FROM month_series;

-- ---------- mart.dim_plan ----------
TRUNCATE TABLE mart.dim_plan;
INSERT INTO mart.dim_plan(plan_id, plan_key, plan_name, plan_rank, base_monthly_price, location_add_on_price, is_active)
SELECT plan_id, plan_key, plan_name, plan_rank, base_monthly_price, location_add_on_price, is_active
FROM staging.plan_catalog;

-- ---------- mart.dim_customer ----------
TRUNCATE TABLE mart.dim_customer;
INSERT INTO mart.dim_customer(customer_id, segment, signup_date, initial_plan_key, initial_contract_type, initial_locations, status, signup_month)
SELECT
	customer_id,
	segment,
	signup_date,
	initial_plan_key,
	initial_contract_type,
	initial_locations,
	status,
	DATE_TRUNC('month', signup_date)::DATE AS signup_month
FROM staging.customers;