from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "delivery_data.csv"


def main():
    rng = np.random.default_rng(42)
    row_count = 1500
    cities = np.array(["Austin", "Chicago", "Denver", "Seattle"])
    categories = np.array(["Asian", "Burgers", "Healthy", "Mexican", "Pizza"])
    channels = np.array(["Organic", "Paid social", "Referral"])
    statuses = rng.choice(["Delivered", "Cancelled"], row_count, p=[0.92, 0.08])
    city = rng.choice(cities, row_count)
    category = rng.choice(categories, row_count)
    channel = rng.choice(channels, row_count, p=[0.48, 0.32, 0.20])
    order_dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(
        rng.integers(0, 120 * 24, row_count), unit="h"
    )
    promised_minutes = rng.choice([30, 40, 50], row_count, p=[0.25, 0.50, 0.25])
    delivery_minutes = np.maximum(
        10, np.rint(rng.normal(35, 10, row_count))
    ).astype(float)
    delivered = statuses == "Delivered"
    delivery_minutes[~delivered] = np.nan

    ratings = np.full(row_count, np.nan)
    rating_values = 4.6 - np.maximum(
        delivery_minutes[delivered] - promised_minutes[delivered], 0
    ) / 12 + rng.normal(0, 0.7, delivered.sum())
    ratings[delivered] = np.clip(np.rint(rating_values), 1, 5)

    data = pd.DataFrame(
        {
            "order_id": [f"ORD-{number:05d}" for number in range(1, row_count + 1)],
            "order_date": order_dates,
            "city": city,
            "restaurant_category": category,
            "acquisition_channel": channel,
            "order_value": np.round(rng.gamma(2.5, 18, row_count), 2),
            "promised_minutes": promised_minutes,
            "delivery_minutes": delivery_minutes,
            "customer_rating": ratings,
            "order_status": statuses,
        }
    )
    data.to_csv(DATA_PATH, index=False)
    print(f"Generated {len(data):,} orders at {DATA_PATH}")


if __name__ == "__main__":
    main()