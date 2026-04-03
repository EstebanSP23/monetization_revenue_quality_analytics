-- ============================================
-- 06_create_vw_monthly_discount_profile.sql
-- Layer: MART
-- Purpose:
--   Create a monthly discount profile view with one row per month_start.
--   The view summarizes discount usage across active customers and active billed MRR,
--   including customer counts with and without discounts, average discount_pct,
--   discounted vs non-discounted MRR, and the share of MRR under discount.
--   This helps evaluate how dependent revenue is on discounting over time.
-- ============================================

DROP VIEW IF EXISTS mart.vw_monthly_discount_profile;
CREATE VIEW mart.vw_monthly_discount_profile AS
SELECT
	month_start,
	COUNT(*) 																		AS active_customers,
	COUNT(*) FILTER (WHERE discount_pct > 0)										AS customers_with_discount,
	COUNT(*) FILTER (WHERE discount_pct = 0)  										AS customers_without_discount,
	COALESCE(AVG(discount_pct) , 0)													AS avg_discount_pct,
	COALESCE(SUM(billed_mrr) FILTER (WHERE discount_pct > 0), 0)					AS discounted_mrr,
	COALESCE(SUM(billed_mrr) FILTER (WHERE discount_pct = 0), 0)					AS non_discounted_mrr,
	COALESCE(
		(SUM(billed_mrr) FILTER (WHERE discount_pct > 0)) / NULLIF(SUM(billed_mrr), 0)
		)																			AS pct_mrr_discounted
FROM mart.fact_customer_month
WHERE is_active = TRUE
GROUP BY month_start;