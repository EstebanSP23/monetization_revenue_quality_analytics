import pandas as pd

from config import PLANS


def generate_plan_catalog() -> pd.DataFrame:
    """
    Build the plan catalog table from config settings.
    """
    rows = []

    for plan_key, plan_info in PLANS.items():
        rows.append(
            {
                "plan_id": plan_info["plan_id"],
                "plan_key": plan_key,
                "plan_name": plan_info["plan_name"],
                "plan_rank": plan_info["plan_rank"],
                "base_monthly_price": plan_info["base_monthly_price"],
                "location_add_on_price": plan_info["location_add_on_price"],
                "is_active": True,
            }
        )

    df = pd.DataFrame(rows).sort_values("plan_id").reset_index(drop=True)
    return df