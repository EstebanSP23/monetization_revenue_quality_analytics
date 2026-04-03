-- ============================================
-- 07_create_vw_monthly_monetization_mix.sql
-- Layer: MART
-- Purpose:
--   Create a monthly monetization mix view with one row per
--   month_start, segment, plan_name, and contract_type.
--   The view summarizes active customer counts, location volume,
--   list MRR, billed MRR, discount amount, and average discount_pct
--   to show where monetization is coming from across the business mix.
-- ============================================

DROP VIEW IF EXISTS mart.vw_monthly_monetization_mix;
CREATE VIEW mart.vw_monthly_monetization_mix AS
SELECT
	cm.month_start,
	c.segment,
	p.plan_name,
	cm.contract_type,
	ROUND(SUM(cm.list_mrr), 2)					AS list_mrr,
	COUNT(DISTINCT cm.customer_id)				AS active_customers,
	SUM(cm.locations)							AS total_locations,
	ROUND(SUM(cm.billed_mrr), 2)				AS billed_mrr,
	ROUND(SUM(cm.list_mrr - cm.billed_mrr), 2)	AS discount_amount,
	ROUND(AVG(cm.discount_pct), 4)				AS avg_discount_pct
FROM mart.fact_customer_month cm
JOIN mart.dim_customer c
	ON cm.customer_id = c.customer_id
JOIN mart.dim_plan p
	ON p.plan_id = cm.plan_id
WHERE cm.is_active = TRUE
GROUP BY
	cm.month_start,
	c.segment,
	p.plan_name,
	cm.contract_type;