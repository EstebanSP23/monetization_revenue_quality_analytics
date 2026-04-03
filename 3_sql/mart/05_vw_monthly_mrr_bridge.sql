-- ============================================
-- 05_create_vw_monthly_mrr_bridge.sql
-- Layer: MART
-- Purpose:
--   Create a reconciled monthly MRR bridge with one row per month_start.
--   The view shows:
--     beginning_mrr
--   + new_mrr
--   + expansion_mrr
--   - contraction_mrr
--   - churn_mrr
--   = ending_mrr
--   It also includes calculated_ending_mrr and bridge_diff to validate that monthly revenue movements reconcile correctly.
-- ============================================

DROP VIEW IF EXISTS mart.vw_monthly_mrr_bridge;

CREATE VIEW mart.vw_monthly_mrr_bridge AS 
WITH monthly AS (
	SELECT
		month_start,
		COALESCE(SUM(billed_mrr), 0) 													AS ending_mrr,
		COALESCE(SUM(mrr_change) FILTER (WHERE movement_type = 'new'), 0)				AS new_mrr,
		COALESCE(SUM(mrr_change) FILTER (WHERE movement_type = 'expansion'), 0)			AS expansion_mrr,
		COALESCE(SUM(ABS(mrr_change)) FILTER (WHERE movement_type = 'contraction'), 0) 	AS contraction_mrr,
		COALESCE(SUM(ABS(mrr_change)) FILTER (WHERE movement_type = 'churn'), 0) 		AS churn_mrr,
		COALESCE(SUM(mrr_change), 0)													AS net_mrr_change
	FROM mart.fact_customer_month
	GROUP BY month_start
),
bridge AS (
	SELECT
		month_start,
		ending_mrr,
		new_mrr,
		expansion_mrr,
		contraction_mrr,
		churn_mrr,
		net_mrr_change,
		LAG(ending_mrr) OVER (ORDER BY month_start) 									AS beginning_mrr
	FROM monthly
)
SELECT
	month_start,
	COALESCE(beginning_mrr, 0) AS beginning_mrr,
	new_mrr,
	expansion_mrr,
	contraction_mrr,
	churn_mrr,
	ending_mrr,
	net_mrr_change,
	(COALESCE(beginning_mrr, 0) + new_mrr + expansion_mrr - contraction_mrr - churn_mrr) 	AS calculated_ending_mrr,
	(ending_mrr) - (COALESCE(beginning_mrr, 0) + new_mrr + expansion_mrr - contraction_mrr - churn_mrr)	AS bridge_diff
FROM bridge
ORDER BY month_start;