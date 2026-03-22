import random
import pandas as pd

from config import END_DATE, EXPANSION_PROBS, CONTRACTION_PROBS


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


def calculate_list_mrr(base_monthly_price: float, location_add_on_price: float, locations: int) -> float:
    extra_locations = max(locations - 1, 0)
    return round(base_monthly_price + (extra_locations * location_add_on_price), 2)


def simulate_lifecycle(
    customers_df: pd.DataFrame,
    subscriptions_df: pd.DataFrame,
    plan_catalog_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    customer_segment_lookup = customers_df.set_index("customer_id")["segment"].to_dict()

    plan_lookup = (
        plan_catalog_df.set_index("plan_key")[
            ["plan_id", "base_monthly_price", "location_add_on_price"]
        ].to_dict(orient="index")
    )

    updated_subscriptions = []
    lifecycle_events = []

    subscription_counter = 1
    event_counter = 1

    for row in subscriptions_df.itertuples(index=False):
        customer_id = row.customer_id
        segment = customer_segment_lookup[customer_id]
        plan_key = row.plan_key
        contract_type = row.contract_type
        discount_pct = row.discount_pct
        current_locations = row.locations

        churn_prob = CHURN_PROBS[(segment, plan_key, contract_type)]
        expansion_prob = EXPANSION_PROBS[(segment, plan_key, contract_type)]
        contraction_prob = CONTRACTION_PROBS[(segment, plan_key, contract_type)]

        signup_month = pd.to_datetime(row.start_date).to_period("M").to_timestamp()
        end_month = pd.Timestamp(END_DATE).to_period("M").to_timestamp()
        month_range = pd.date_range(start=signup_month, end=end_month, freq="MS")

        state_start = signup_month

        for i, month_start in enumerate(month_range):
            if i == 0:
                continue

            movement = "flat"

            if random.random() < churn_prob:
                movement = "churn"
            else:
                if random.random() < expansion_prob:
                    movement = "expansion"
                elif current_locations > 1 and random.random() < contraction_prob:
                    movement = "contraction"

            if movement == "flat":
                continue

            base_price = plan_lookup[plan_key]["base_monthly_price"]
            add_on_price = plan_lookup[plan_key]["location_add_on_price"]

            previous_list_mrr = calculate_list_mrr(base_price, add_on_price, current_locations)
            previous_billed_mrr = round(previous_list_mrr * (1 - discount_pct), 2)

            if movement == "churn":
                updated_subscriptions.append(
                    {
                        "subscription_id": f"SUB_{subscription_counter:05d}",
                        "customer_id": customer_id,
                        "plan_id": row.plan_id,
                        "plan_key": plan_key,
                        "contract_type": contract_type,
                        "start_date": state_start.date(),
                        "end_date": month_start.date(),
                        "locations": current_locations,
                        "discount_pct": discount_pct,
                        "list_mrr": previous_list_mrr,
                        "billed_mrr": previous_billed_mrr,
                        "is_active": False,
                    }
                )
                subscription_counter += 1

                lifecycle_events.append(
                    {
                        "event_id": f"EVT_{event_counter:05d}",
                        "customer_id": customer_id,
                        "subscription_id": None,
                        "event_date": month_start.date(),
                        "event_type": "churn",
                        "old_plan_id": row.plan_id,
                        "new_plan_id": None,
                        "old_locations": current_locations,
                        "new_locations": None,
                        "old_discount_pct": discount_pct,
                        "new_discount_pct": None,
                    }
                )
                event_counter += 1
                break

            new_locations = current_locations + 1 if movement == "expansion" else current_locations - 1

            updated_subscriptions.append(
                {
                    "subscription_id": f"SUB_{subscription_counter:05d}",
                    "customer_id": customer_id,
                    "plan_id": row.plan_id,
                    "plan_key": plan_key,
                    "contract_type": contract_type,
                    "start_date": state_start.date(),
                    "end_date": month_start.date(),
                    "locations": current_locations,
                    "discount_pct": discount_pct,
                    "list_mrr": previous_list_mrr,
                    "billed_mrr": previous_billed_mrr,
                    "is_active": False,
                }
            )
            subscription_counter += 1

            new_list_mrr = calculate_list_mrr(base_price, add_on_price, new_locations)
            new_billed_mrr = round(new_list_mrr * (1 - discount_pct), 2)

            lifecycle_events.append(
                {
                    "event_id": f"EVT_{event_counter:05d}",
                    "customer_id": customer_id,
                    "subscription_id": None,
                    "event_date": month_start.date(),
                    "event_type": movement,
                    "old_plan_id": row.plan_id,
                    "new_plan_id": row.plan_id,
                    "old_locations": current_locations,
                    "new_locations": new_locations,
                    "old_discount_pct": discount_pct,
                    "new_discount_pct": discount_pct,
                }
            )
            event_counter += 1

            current_locations = new_locations
            state_start = month_start

        else:
            base_price = plan_lookup[plan_key]["base_monthly_price"]
            add_on_price = plan_lookup[plan_key]["location_add_on_price"]

            final_list_mrr = calculate_list_mrr(base_price, add_on_price, current_locations)
            final_billed_mrr = round(final_list_mrr * (1 - discount_pct), 2)

            updated_subscriptions.append(
                {
                    "subscription_id": f"SUB_{subscription_counter:05d}",
                    "customer_id": customer_id,
                    "plan_id": row.plan_id,
                    "plan_key": plan_key,
                    "contract_type": contract_type,
                    "start_date": state_start.date(),
                    "end_date": None,
                    "locations": current_locations,
                    "discount_pct": discount_pct,
                    "list_mrr": final_list_mrr,
                    "billed_mrr": final_billed_mrr,
                    "is_active": True,
                }
            )
            subscription_counter += 1

    updated_subscriptions_df = (
        pd.DataFrame(updated_subscriptions)
        .sort_values(["customer_id", "start_date", "subscription_id"])
        .reset_index(drop=True)
    )

    lifecycle_events_df = (
        pd.DataFrame(lifecycle_events)
        .sort_values(["event_date", "customer_id", "event_type"])
        .reset_index(drop=True)
    )

    return updated_subscriptions_df, lifecycle_events_df