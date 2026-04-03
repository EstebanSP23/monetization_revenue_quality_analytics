-- ============================================
-- 08_create_vw_monthly_expansion_profile.sql
-- Layer: MART
-- Purpose:
--   Create a monthly expansion profile view with one row per
--   month_start, segment, plan_name, and contract_type.
--   The view summarizes expansion activity across the business mix,
--   including expanding customers, expansion events, expansion MRR,
--   post-expansion location volume, and average expansion MRR per customer.
--   This helps isolate where growth from expansion is coming from over time.
-- ============================================

DROP VIEW IF EXISTS mart.vw_monthly_expansion_profile;
CREATE VIEW mart.vw_monthly_expansion_profile AS
SELECT
	cm.month_start,
	c.segment													AS segment,
	p.plan_name													AS plan_name,
	cm.contract_type											AS contract_type,
	COUNT(DISTINCT cm.customer_id)								AS expanding_customers,
	COUNT(*)													AS expansion_events,
	ROUND(SUM(cm.mrr_change), 2)								AS expansion_mrr,
	SUM(cm.locations)											AS total_locations_post_exp,
	ROUND(AVG(cm.mrr_change), 2)								AS avg_expansion_mrr_per_customer
FROM mart.fact_customer_month cm
JOIN mart.dim_customer c
	ON cm.customer_id = c.customer_id
JOIN mart.dim_plan p
	ON p.plan_id = cm.plan_id
WHERE cm.movement_type = 'expansion' AND cm.is_active = TRUE
GROUP BY cm.month_start, c.segment, p.plan_name, cm.contract_type
ORDER BY cm.month_start;

SELECT *
FROM mart.vw_monthly_expansion_profile;