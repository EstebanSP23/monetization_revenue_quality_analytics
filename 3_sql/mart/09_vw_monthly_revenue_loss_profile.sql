-- ============================================
-- 09_create_vw_monthly_revenue_loss_profile.sql
-- Layer: MART
-- Purpose:
--   Create a monthly revenue loss profile view with one row per
--   month_start, segment, plan_name, and contract_type.
--   The view summarizes contraction and churn activity across the
--   business mix, including affected customers, loss events,
--   contraction MRR, churn MRR, and total revenue loss MRR.
--   This helps isolate where revenue leakage is coming from over time.
-- ============================================

DROP VIEW IF EXISTS mart.vw_monthly_revenue_loss_profile;
CREATE VIEW mart.vw_monthly_revenue_loss_profile AS
SELECT
	cm.month_start,
	c.segment,
	p.plan_name,
	cm.contract_type,
	COUNT(*)																						AS revenue_loss_events,
	COUNT(DISTINCT cm.customer_id)																	AS customers_with_revenue_loss,
	COUNT(*) FILTER (WHERE cm.movement_type = 'contraction')										AS contraction_events,
	COUNT(DISTINCT cm.customer_id) FILTER (WHERE cm.movement_type = 'contraction')					AS contraction_customers,
	COALESCE(ROUND(SUM(ABS(cm.mrr_change)) FILTER (WHERE cm.movement_type = 'contraction'), 2), 0)	AS contraction_mrr,
	COUNT(*) FILTER (WHERE cm.movement_type = 'churn')												AS churn_events,
	COUNT(DISTINCT cm.customer_id) FILTER (WHERE cm.movement_type = 'churn')						AS churned_customers,
	COALESCE(ROUND(SUM(ABS(cm.mrr_change)) FILTER (WHERE cm.movement_type = 'churn'), 2), 0)		AS churn_mrr,
	ROUND(SUM(ABS(cm.mrr_change)), 2)																AS total_revenue_loss_mrr
FROM mart.fact_customer_month cm
JOIN mart.dim_customer c
	ON cm.customer_id = c.customer_id
JOIN mart.dim_plan p
	ON cm.plan_id = p.plan_id
WHERE cm.movement_type IN ('contraction', 'churn')
GROUP BY cm.month_start, c.segment, p.plan_name, cm.contract_type
ORDER BY cm.month_start;