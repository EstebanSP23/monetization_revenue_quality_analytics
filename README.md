# Monetization & Revenue Quality Analytics

### Production-Style Monetization Analytics System for a B2B Fitness SaaS Business

---

## 1. Executive Summary

**Monetization & Revenue Quality Analytics** is a production-style analytics project built to evaluate whether a B2B fitness SaaS business is growing through **healthy monetization** or through **weak pricing discipline**.

The project answers a core executive question:

**Is revenue growth being driven by healthy pricing and expansion, or by weak discounting and low-quality monetization?**

To answer that question, the system analyzes:

- Pricing tier performance
- Discounting behavior
- Expansion and contraction revenue
- Customer churn
- Revenue quality by segment
- Contract mix (monthly vs annual)
- Monthly recurring revenue (MRR) movement over time

The dataset is synthetic, but it is intentionally designed to simulate realistic subscription behavior for a B2B fitness SaaS company serving gyms, studios, and multi-location fitness businesses.

---

## 2. Business Context

The fictional company sells subscription software to fitness businesses to help manage:

- Memberships
- Scheduling
- Billing
- Retention tracking
- Business performance reporting

Customer segments include:

- **Small**
- **Mid**
- **Large**

The monetization model includes:

- 3 pricing plans: **Basic, Pro, Enterprise**
- Monthly and annual contracts
- Discounting at acquisition and renewal
- Expansion and contraction through location changes
- Churn over time

This project focuses on **revenue quality**, not just revenue volume.

---

## 3. Business Objective

The purpose of this project is to build an analytics system that helps answer questions such as:

- Is headline growth supported by healthy expansion, or weakened by heavy discounting?
- How much revenue growth comes from new business vs existing customer expansion?
- How much revenue is leaking through contraction and churn?
- Which segments, plans, and contract types monetize most effectively?
- Is growth becoming more dependent on discounted revenue over time?

---

## 4. Architecture Overview

```text
Python Synthetic Data Generation
        |
        v
Raw CSV Files
        |
        v
PostgreSQL
-----------------------------------
RAW Layer
  - raw.plan_catalog
  - raw.customers
  - raw.subscriptions
  - raw.subscription_events
  - raw.customer_month
-----------------------------------
STAGING Layer
  - staging.plan_catalog
  - staging.customers
  - staging.subscriptions
  - staging.subscription_events
  - staging.customer_month
-----------------------------------
MART Layer
  Dimensions
    - mart.dim_date
    - mart.dim_plan
    - mart.dim_customer

  Core Fact
    - mart.fact_customer_month

  Analytical Views
    - mart.vw_monthly_mrr_bridge
    - mart.vw_monthly_discount_profile
    - mart.vw_monthly_monetization_mix
    - mart.vw_monthly_expansion_profile
    - mart.vw_monthly_revenue_loss_profile
        |
        v
Power BI
  - Executive dashboard
  - Monetization mix analysis
  - Expansion and revenue loss diagnostics
```

---

## 5. Synthetic Business Model Assumptions

### Business Setup

- **Industry:** B2B Fitness SaaS
- **Date range:** Jan 2023 - Dec 2025
- **Synthetic customers:** 7,000
- **Customer segments:** Small, Mid, Large

### Pricing Model

#### Plans
- **Basic:** $99
- **Pro:** $299 + $40 per extra location
- **Enterprise:** $799 + $70 per extra location

#### Contracts
- Monthly
- Annual

#### Discount Bands
- 0%
- 10%
- 20%
- 30%

### Behavioral Assumptions

- Smaller businesses churn more than larger ones
- Annual contracts retain better than monthly contracts
- Expansion and contraction happen through changes in number of locations
- Heavier discounting is treated as a signal of weaker monetization quality

---

## 6. Data Pipeline Layers

## RAW Layer

The RAW layer stores the CSV data exactly as loaded from Python-generated files, with no business logic applied.

### Tables
- `raw.plan_catalog`
- `raw.customers`
- `raw.subscriptions`
- `raw.subscription_events`
- `raw.customer_month`

---

## STAGING Layer

The STAGING layer stores trusted, analytics-ready versions of the raw tables.

Its purpose is to:

- Preserve clean structure
- Enforce key constraints where needed
- Prepare consistent inputs for downstream business analysis

### Tables
- `staging.plan_catalog`
- `staging.customers`
- `staging.subscriptions`
- `staging.subscription_events`
- `staging.customer_month`

---

## MART Layer

The MART layer stores business-facing dimensions, fact tables, and analytical views used for reporting and diagnosis.

### Dimensions
- `mart.dim_date`
- `mart.dim_plan`
- `mart.dim_customer`

### Core Fact Table
- `mart.fact_customer_month`

**Grain:** one row per customer per month

This is the central fact table for analyzing recurring revenue behavior, monetization quality, and revenue movement over time.

---

## 7. Core MART Views

### `mart.vw_monthly_mrr_bridge`
Creates a reconciled monthly MRR bridge showing:

- Beginning MRR
- New MRR
- Expansion MRR
- Contraction MRR
- Churn MRR
- Ending MRR

This view validates that monthly revenue movements reconcile correctly.

---

### `mart.vw_monthly_discount_profile`
Summarizes monthly discount usage across active customers and billed MRR, including:

- Active customers
- Customers with and without discounts
- Average discount rate
- Discounted MRR
- Non-discounted MRR
- Share of MRR under discount

This view helps evaluate how dependent revenue is on discounting over time.

---

### `mart.vw_monthly_monetization_mix`
Breaks monetization down by:

- Month
- Segment
- Plan
- Contract type

This view shows where revenue, discounting, and customer volume are concentrated across the business mix.

---

### `mart.vw_monthly_expansion_profile`
Isolates monthly expansion activity across the business mix, including:

- Expanding customers
- Expansion events
- Expansion MRR
- Post-expansion locations
- Average expansion MRR per customer

This view helps identify where expansion-driven growth is strongest.

---

### `mart.vw_monthly_revenue_loss_profile`
Isolates contraction and churn across the business mix, including:

- Customers with revenue loss
- Revenue loss events
- Contraction MRR
- Churn MRR
- Total revenue loss MRR

This view helps identify where revenue leakage is most concentrated.

---

## 8. Power BI Reporting Layer

The Power BI dashboard is designed as a 3-page executive and diagnostic reporting layer.

### Page 1 — Executive Overview
Focuses on overall growth health and pricing pressure.

Includes:
- Ending MRR
- Net MRR change
- New, expansion, contraction, and churn MRR
- % of MRR under discount
- Revenue movement trend
- Discount dependence trend

### Page 2 — Monetization Mix
Shows where monetization is coming from across the business.

Includes:
- Active customers
- Billed MRR
- Average discount %
- Total locations
- Revenue by segment
- Revenue by plan
- Customer and pricing mix diagnostics

### Page 3 — Expansion & Revenue Loss
Shows the push-pull dynamic between growth and leakage.

Includes:
- Expansion MRR
- Contraction MRR
- Churn MRR
- Customers with revenue loss
- Expansion vs revenue loss over time
- Segment-level and plan-level revenue leakage diagnostics

---

## 9. Key Skills Demonstrated

This project is designed to showcase:

- Production-style analytics workflow
- Synthetic but business-driven data generation
- Layered SQL architecture (**RAW -> STAGING -> MART**)
- Fact/dimension modeling
- Revenue movement and reconciliation logic
- Customer-month subscription modeling
- Monetization and pricing diagnostics
- Executive-oriented Power BI reporting
- Clear separation of generation, storage, transformation, and presentation layers

---

## 10. Repository Structure

```text
0_project_admin/
1_data_generation/
2_data/
    raw/
    processed/
3_sql/
    raw/
    staging/
    mart/
    validation/
4_power_bi/
    pbix/
    screenshots/
5_outputs/
	README.md
```

---

## 11. Current Outputs

### Generated Raw Files
- `plan_catalog.csv`
- `customers.csv`
- `subscriptions.csv`
- `subscription_events.csv`
- `customer_month.csv`

### SQL Outputs
- RAW tables
- STAGING tables
- MART dimensions
- MART fact table
- Analytical MART views

### Reporting Outputs
- Power BI dashboard
- Screenshots
- Final project documentation

All outputs are reproducible through a fixed-seed Python generation process.

---

## 12. How to Reproduce the Project

1. Run the Python synthetic data generator
2. Generate raw CSV files into `2_data/raw/`
3. Load raw CSVs into PostgreSQL RAW tables
4. Execute the SQL pipeline scripts for:
   - RAW
   - STAGING
   - MART dimensions
   - MART fact table
   - MART analytical views
5. Connect Power BI to the MART layer
6. Build the dashboard using the validated analytical views and fact table

---

## 13. Why This Project Matters

This project goes beyond a generic recurring revenue dashboard.

It is designed to reflect how a business would actually evaluate monetization quality by asking:

- Is discounting helping growth, or weakening pricing discipline?
- Is expansion strong enough to offset revenue leakage?
- Are some segments monetizing more effectively than others?
- Is reported growth supported by healthy fundamentals?

The goal is to build a business-relevant analytics system that feels closer to real monetization analysis work than to a simple visualization exercise.

---

## 14. Tools Used

- **Python** - synthetic data generation
- **PostgreSQL** - layered data modeling and transformation
- **Power BI** - executive reporting and diagnostics
- **Git / GitHub** - version control and project presentation

---

*Project by [EstebanSP23](https://github.com/EstebanSP23) – Data Analytics Portfolio*

