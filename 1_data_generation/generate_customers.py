from datetime import timedelta
import random

import pandas as pd

from config import (
    END_DATE,
    INITIAL_CONTRACT_PROBS,
    INITIAL_LOCATIONS,
    INITIAL_LOCATION_WEIGHTS,
    INITIAL_PLAN_PROBS,
    N_CUSTOMERS,
    SEGMENT_MIX,
    START_DATE,
)


def weighted_choice(prob_dict: dict) -> str:
    choices = list(prob_dict.keys())
    weights = list(prob_dict.values())
    return random.choices(choices, weights=weights, k=1)[0]


def random_signup_date():
    total_days = (END_DATE - START_DATE).days
    random_days = random.randint(0, total_days)
    return START_DATE + timedelta(days=random_days)


def generate_customers() -> pd.DataFrame:
    rows = []

    segment_choices = list(SEGMENT_MIX.keys())
    segment_weights = list(SEGMENT_MIX.values())

    for i in range(1, N_CUSTOMERS + 1):
        customer_id = f"CUST_{i:05d}"

        segment = random.choices(segment_choices, weights=segment_weights, k=1)[0]
        signup_date = random_signup_date()

        initial_plan_key = weighted_choice(INITIAL_PLAN_PROBS[segment])
        initial_contract_type = weighted_choice(INITIAL_CONTRACT_PROBS[segment])

        initial_locations = random.choices(
            INITIAL_LOCATIONS[segment],
            weights=INITIAL_LOCATION_WEIGHTS[segment],
            k=1,
        )[0]

        rows.append(
            {
                "customer_id": customer_id,
                "segment": segment,
                "signup_date": signup_date,
                "initial_plan_key": initial_plan_key,
                "initial_contract_type": initial_contract_type,
                "initial_locations": initial_locations,
                "status": "active",
            }
        )

    df = pd.DataFrame(rows).sort_values("customer_id").reset_index(drop=True)
    return df