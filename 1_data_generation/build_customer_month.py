import pandas as pd

from config import END_DATE


def build_customer_month(subscriptions_df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for row in subscriptions_df.itertuples(index=False):
        signup_month = pd.to_datetime(row.start_date).to_period("M").to_timestamp()
        end_month = pd.Timestamp(END_DATE).to_period("M").to_timestamp()

        month_range = pd.date_range(start=signup_month, end=end_month, freq="MS")

        prev_billed_mrr = None

        for i, month_start in enumerate(month_range):
            billed_mrr = row.billed_mrr

            if i == 0:
                movement_type = "new"
                mrr_change = billed_mrr
            else:
                movement_type = "flat"
                mrr_change = billed_mrr - prev_billed_mrr

            rows.append(
                {
                    "month_start": month_start.date(),
                    "customer_id": row.customer_id,
                    "plan_id": row.plan_id,
                    "contract_type": row.contract_type,
                    "locations": row.locations,
                    "list_mrr": row.list_mrr,
                    "discount_pct": row.discount_pct,
                    "billed_mrr": billed_mrr,
                    "prev_billed_mrr": prev_billed_mrr,
                    "mrr_change": round(mrr_change, 2) if mrr_change is not None else None,
                    "movement_type": movement_type,
                    "is_active": True,
                }
            )

            prev_billed_mrr = billed_mrr

    df = pd.DataFrame(rows).sort_values(["customer_id", "month_start"]).reset_index(drop=True)
    return df