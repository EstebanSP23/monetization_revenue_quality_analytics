# Project configuration for synthetic data generation

from datetime import date

# =========================
# Project scope
# =========================
N_CUSTOMERS = 7000

START_DATE = date(2023, 1, 1)
END_DATE = date(2025, 12, 31)

# =========================
# Plans
# =========================
PLANS = {
    "basic": {
        "plan_id": 1,
        "plan_name": "Basic",
        "plan_rank": 1,
        "base_monthly_price": 99,
        "location_add_on_price": 0,
    },
    "pro": {
        "plan_id": 2,
        "plan_name": "Pro",
        "plan_rank": 2,
        "base_monthly_price": 299,
        "location_add_on_price": 40,
    },
    "enterprise": {
        "plan_id": 3,
        "plan_name": "Enterprise",
        "plan_rank": 3,
        "base_monthly_price": 799,
        "location_add_on_price": 70,
    },
}

# =========================
# Segments
# =========================
SEGMENTS = ["small", "mid_sized", "large"]

SEGMENT_MIX = {
    "small": 0.60,
    "mid_sized": 0.30,
    "large": 0.10,
}

# =========================
# Contracts
# =========================
CONTRACT_TYPES = ["monthly", "annual"]

# =========================
# Discount bands
# =========================
DISCOUNT_BANDS = [0.00, 0.10, 0.20, 0.30]

# =========================
# Initial plan probabilities
# Locations influence fit,
# but are not a hard rule
# =========================
INITIAL_PLAN_PROBS = {
    "small": {
        "basic": 0.85,
        "pro": 0.14,
        "enterprise": 0.01,
    },
    "mid_sized": {
        "basic": 0.10,
        "pro": 0.80,
        "enterprise": 0.10,
    },
    "large": {
        "basic": 0.02,
        "pro": 0.23,
        "enterprise": 0.75,
    },
}

# =========================
# Initial contract probabilities
# =========================
INITIAL_CONTRACT_PROBS = {
    "small": {
        "monthly": 0.75,
        "annual": 0.25,
    },
    "mid_sized": {
        "monthly": 0.45,
        "annual": 0.55,
    },
    "large": {
        "monthly": 0.20,
        "annual": 0.80,
    },
}

# =========================
# Initial locations
# Weighted choices by segment
# =========================
INITIAL_LOCATIONS = {
    "small": [1],
    "mid_sized": [2, 3, 4, 5],
    "large": [6, 7, 8, 9, 10],
}

INITIAL_LOCATION_WEIGHTS = {
    "small": [1.0],
    "mid_sized": [0.35, 0.30, 0.20, 0.15],
    "large": [0.30, 0.25, 0.20, 0.15, 0.10],
}

# =========================
# Acquisition discount probabilities
# by segment and contract type
# =========================
ACQUISITION_DISCOUNT_PROBS = {
    "small": {
        "monthly": {0.00: 0.80, 0.10: 0.18, 0.20: 0.02, 0.30: 0.00},
        "annual":  {0.00: 0.60, 0.10: 0.30, 0.20: 0.09, 0.30: 0.01},
    },
    "mid_sized": {
        "monthly": {0.00: 0.60, 0.10: 0.28, 0.20: 0.10, 0.30: 0.02},
        "annual":  {0.00: 0.40, 0.10: 0.35, 0.20: 0.20, 0.30: 0.05},
    },
    "large": {
        "monthly": {0.00: 0.45, 0.10: 0.30, 0.20: 0.20, 0.30: 0.05},
        "annual":  {0.00: 0.25, 0.10: 0.35, 0.20: 0.30, 0.30: 0.10},
    },
}