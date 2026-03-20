import pandas as pd

from config import ACQUISITION_DISCOUNT_PROBS


def weighted_choice(prob_dict: dict):
    import random

    choices = list(prob_dict.keys())
    weights = list(prob_dict.values())
    return random.choices(choices, weights=weights, k=1)[0]


def calculate_list_mrr(plan_catalog_lookup: dict, plan_key: str, locations: int) -> float:
    plan = plan_catalog_lookup[plan_key]
    base_price = plan["base_monthly_price"]
    add_on_price = plan["location_add_on_price"]

    extra_locations = max(locations - 1, 0)
    list_mrr = base_price + (extra_locations * add_on_price)
    return float(list_mrr)


def generate_initial_subscriptions(
    customers_df: pd.DataFrame,
    plan_catalog_df: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    plan_catalog_lookup = (
        plan_catalog_df.set_index("plan_key")[
            ["plan_id", "base_monthly_price", "location_add_on_price"]
        ].to_dict(orient="index")
    )

    for i, row in enumerate(customers_df.itertuples(index=False), start=1):
        discount_pct = weighted_choice(
            ACQUISITION_DISCOUNT_PROBS[row.segment][row.initial_contract_type]
        )

        list_mrr = calculate_list_mrr(
            plan_catalog_lookup=plan_catalog_lookup,
            plan_key=row.initial_plan_key,
            locations=row.initial_locations,
        )

        billed_mrr = round(list_mrr * (1 - discount_pct), 2)

        rows.append(
            {
                "subscription_id": f"SUB_{i:05d}",
                "customer_id": row.customer_id,
                "plan_id": plan_catalog_lookup[row.initial_plan_key]["plan_id"],
                "plan_key": row.initial_plan_key,
                "contract_type": row.initial_contract_type,
                "start_date": row.signup_date,
                "end_date": None,
                "locations": row.initial_locations,
                "discount_pct": discount_pct,
                "list_mrr": round(list_mrr, 2),
                "billed_mrr": billed_mrr,
                "is_active": True,
            }
        )

    df = pd.DataFrame(rows).sort_values("customer_id").reset_index(drop=True)
    return df