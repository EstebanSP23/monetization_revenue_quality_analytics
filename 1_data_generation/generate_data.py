from pathlib import Path

from config import N_CUSTOMERS, START_DATE, END_DATE
from generate_customers import generate_customers
from generate_dimensions import generate_plan_catalog


def main() -> None:
    """
    Main entry point for synthetic data generation.
    """
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "2_data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Starting synthetic data generation...")
    print(f"Customers to generate: {N_CUSTOMERS}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    print(f"Raw output folder: {output_dir}")

    plan_catalog = generate_plan_catalog()
    plan_catalog.to_csv(output_dir / "plan_catalog.csv", index=False)

    customers = generate_customers()
    customers.to_csv(output_dir / "customers.csv", index=False)

    print("Generated: plan_catalog.csv")
    print("Generated: customers.csv")
    print("Generation skeleton ready.")

    # TODO:
    # 1. Generate plan_catalog
    # 2. Generate customers
    # 3. Simulate subscriptions
    # 4. Generate subscription_events
    # 5. Build customer_month
    # 6. Export all tables to CSV

    print("Generation skeleton ready.")


if __name__ == "__main__":
    main()