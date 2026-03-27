import pandas as pd

from config import END_DATE


def build_customer_month(
    subscriptions_df: pd.DataFrame,
    subscription_events_df: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    subscriptions_df = subscriptions_df.copy()
    subscriptions_df["start_date"] = pd.to_datetime(subscriptions_df["start_date"])
    subscriptions_df["end_date"] = pd.to_datetime(
        subscriptions_df["end_date"], errors="coerce"
    )

    subscriptions_df = subscriptions_df.sort_values(
        ["customer_id", "start_date", "subscription_id"]
    ).reset_index(drop=True)

    for row in subscriptions_df.itertuples(index=False):
        start_month = pd.Timestamp(row.start_date).to_period("M").to_timestamp()
        effective_end = (
            row.end_date if pd.notna(row.end_date) else pd.Timestamp(END_DATE)
        )
        end_month = pd.Timestamp(effective_end).to_period("M").to_timestamp()

        month_range = pd.date_range(start=start_month, end=end_month, freq="MS")

        for month_start in month_range:
            rows.append(
                {
                    "month_start": month_start,
                    "customer_id": row.customer_id,
                    "subscription_id": row.subscription_id,
                    "plan_id": row.plan_id,
                    "contract_type": row.contract_type,
                    "locations": row.locations,
                    "list_mrr": row.list_mrr,
                    "discount_pct": row.discount_pct,
                    "billed_mrr": row.billed_mrr,
                    "start_date": row.start_date,
                    "end_date": row.end_date,
                }
            )

    df = pd.DataFrame(rows)

    # Keep only one row per customer-month:
    # the latest subscription state active in that month
    df = (
        df.sort_values(["customer_id", "month_start", "start_date", "subscription_id"])
        .drop_duplicates(subset=["customer_id", "month_start"], keep="last")
        .sort_values(["customer_id", "month_start"])
        .reset_index(drop=True)
    )

    df["prev_billed_mrr"] = df.groupby("customer_id")["billed_mrr"].shift(1)

    churn_months = set()
    if not subscription_events_df.empty:
        churn_events = subscription_events_df[
            subscription_events_df["event_type"] == "churn"
        ].copy()

        if not churn_events.empty:
            churn_events["event_date"] = pd.to_datetime(churn_events["event_date"])
            churn_events["month_start"] = (
                churn_events["event_date"].dt.to_period("M").dt.to_timestamp()
            )
            churn_months = set(
                zip(churn_events["customer_id"], churn_events["month_start"])
            )

    df["is_churn_month"] = df.apply(
        lambda row: (row["customer_id"], row["month_start"]) in churn_months,
        axis=1,
    )

    # Churn month should represent the first zero-revenue month
    df["is_active"] = ~df["is_churn_month"]
    df.loc[df["is_churn_month"], "billed_mrr"] = 0

    def classify_movement(row):
        key = (row["customer_id"], row["month_start"])

        if pd.isna(row["prev_billed_mrr"]):
            return "new"

        if key in churn_months:
            return "churn"

        if row["billed_mrr"] > row["prev_billed_mrr"]:
            return "expansion"

        if row["billed_mrr"] < row["prev_billed_mrr"]:
            return "contraction"

        return "flat"

    df["movement_type"] = df.apply(classify_movement, axis=1)

    def calculate_mrr_change(row):
        if row["movement_type"] == "new":
            return row["billed_mrr"]
        if row["movement_type"] == "churn":
            return -row["prev_billed_mrr"]
        return row["billed_mrr"] - row["prev_billed_mrr"]

    df["mrr_change"] = df.apply(calculate_mrr_change, axis=1).round(2)

    df["month_start"] = df["month_start"].dt.date

    df = df[
        [
            "month_start",
            "customer_id",
            "plan_id",
            "contract_type",
            "locations",
            "list_mrr",
            "discount_pct",
            "billed_mrr",
            "prev_billed_mrr",
            "mrr_change",
            "movement_type",
            "is_active",
        ]
    ]

    return df