import pandas as pd


def generate_signup_events(subscriptions_df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for i, row in enumerate(subscriptions_df.itertuples(index=False), start=1):
        rows.append(
            {
                "event_id": f"EVT_{i:05d}",
                "customer_id": row.customer_id,
                "subscription_id": row.subscription_id,
                "event_date": row.start_date,
                "event_type": "signup",
                "old_plan_id": None,
                "new_plan_id": row.plan_id,
                "old_locations": None,
                "new_locations": row.locations,
                "old_discount_pct": None,
                "new_discount_pct": row.discount_pct,
            }
        )

    df = pd.DataFrame(rows).sort_values(["event_date", "customer_id"]).reset_index(drop=True)
    return df