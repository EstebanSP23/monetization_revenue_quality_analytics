from pathlib import path

from config import N_CUSTOMERS, START_DATE, END_DATE

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