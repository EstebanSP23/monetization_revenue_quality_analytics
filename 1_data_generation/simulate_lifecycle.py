import random

import pandas as pd

from config import END_DATE


CHURN_PROBS = {
    ("small", "basic", "monthly"): 0.032,
    ("small", "basic", "annual"): 0.016,
    ("small", "pro", "monthly"): 0.022,
    ("small", "pro", "annual"): 0.011,
    ("small", "enterprise", "monthly"): 0.015,
    ("small", "enterprise", "annual"): 0.008,

    ("mid", "basic", "monthly"): 0.024,
    ("mid", "basic", "annual"): 0.012,
    ("mid", "pro", "monthly"): 0.016,
    ("mid", "pro", "annual"): 0.008,
    ("mid", "enterprise", "monthly"): 0.011,
    ("mid", "enterprise", "annual"): 0.005,

    ("large", "basic", "monthly"): 0.018,
    ("large", "basic", "annual"): 0.009,
    ("large", "pro", "monthly"): 0.011,
    ("large", "pro", "annual"): 0.005,
    ("large", "enterprise", "monthly"): 0.007,
    ("large", "enterprise", "annual"): 0.003,
}


def simulate_churn_only(
    customers_df: pd.DataFrame,
    subscriptions_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    customer_segment_lookup = customers_df.set_index("customer_id")["segment"].to_dict()

    updated_subscriptions = []
    churn_events = []

    for row in subscriptions_df.itertuples(index=False):
        segment = customer_segment_lookup[row.customer_id]
        plan_key = row.plan_key
        contract_type = row.contract_type

        churn_prob = CHURN_PROBS[(segment, plan_key, contract_type)]

        signup_month = pd.to_datetime(row.start_date).to_period("M").to_timestamp()
        end_month = pd.Timestamp(END_DATE).to_period("M").to_timestamp()
        month_range = pd.date_range(start=signup_month, end=end_month, freq="MS")

        churn_month = None

        for i, month_start in enumerate(month_range):
            if i == 0:
                continue

            if random.random() < churn_prob:
                churn_month = month_start
                break

        row_dict = row._asdict()

        if churn_month is not None:
            row_dict["end_date"] = churn_month.date()
            row_dict["is_active"] = False

            churn_events.append(
                {
                    "event_id": None,
                    "customer_id": row.customer_id,
                    "subscription_id": row.subscription_id,
                    "event_date": churn_month.date(),
                    "event_type": "churn",
                    "old_plan_id": row.plan_id,
                    "new_plan_id": None,
                    "old_locations": row.locations,
                    "new_locations": None,
                    "old_discount_pct": row.discount_pct,
                    "new_discount_pct": None,
                }
            )

        updated_subscriptions.append(row_dict)

    updated_subscriptions_df = pd.DataFrame(updated_subscriptions)
    churn_events_df = pd.DataFrame(churn_events)

    if not churn_events_df.empty:
        churn_events_df["event_id"] = [
            f"EVT_CHURN_{i:05d}" for i in range(1, len(churn_events_df) + 1)
        ]

    return updated_subscriptions_df, churn_events_df