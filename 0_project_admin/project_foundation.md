\# Project Foundation



\## Project Title

Monetization \& Revenue Quality Analytics



\## Business Context

This project simulates a B2B fitness SaaS company that sells subscription software to gyms, studios, and fitness businesses.



The purpose is to evaluate whether revenue growth is being driven by healthy monetization strategy or by weak pricing discipline.



\## Main Business Question

Is our revenue growth driven by healthy pricing and expansion, or by weak discounting and low-quality monetization?



\## Customer Segments

\- Small businesses

\- Mid-sized businesses

\- Large businesses



\## Product Scope

The platform helps fitness businesses manage:

\- memberships

\- scheduling

\- billing

\- retention tracking

\- business performance reporting



\## Plans

\- Basic

\- Pro

\- Enterprise



\### Plan Positioning

\- Basic: best fit for smaller, simpler businesses

\- Pro: best fit for growing, moderately complex businesses

\- Enterprise: best fit for large or high-complexity businesses



Locations influence plan fit, but they are not a hard rule.



\## Contracts

\- Monthly

\- Annual



\## Pricing Logic

Monthly list prices:

\- Basic: $99

\- Pro: $299

\- Enterprise: $799



Location pricing:

\- Basic: flat price

\- Pro: +$40 per additional location after the first

\- Enterprise: +$70 per additional location after the first



Discounts apply to the total recurring price.



\## Discount Logic

Discount bands:

\- 0%

\- 10%

\- 20%

\- 30%



High-level rules:

\- annual contracts are more likely to receive discounts

\- larger accounts are more likely to receive discounts

\- deep discounts should remain relatively rare

\- heavy discounting should be associated with weaker long-term revenue quality



\## Expansion Logic

Expansion can happen through:

\- plan upgrades

\- growth in number of locations



\## Downgrade / Contraction Logic

Contraction can happen through:

\- plan downgrades

\- reduction in number of locations



\## Churn Logic

Churn means the customer cancels and stops paying.



High-level assumptions:

\- smaller businesses churn more than larger businesses

\- monthly contracts churn more than annual contracts

\- lower-tier plans churn more than higher-tier plans



\## Main Analytical Unit

One row per customer account per month.



\## Core Analytical Focus

\- pricing tier performance

\- discount effectiveness

\- upgrades and downgrades

\- expansion revenue

\- contraction revenue

\- retention quality

\- revenue quality by segment

\- contract effect on revenue stability



\## Exclusions

\- lifetime plan

\- physical inventory logic

\- consumer app behavior

\- machine learning

\- forecasting

\- highly detailed billing edge cases



\## MVP Principle

Keep the project believable, analytically strong, and simple enough to complete cleanly.

