from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "delivery_data.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"


def summarize_segment(orders, delivered, segment):
    totals = orders.groupby(segment).agg(
        orders=("order_id", "count"),
        cancellation_rate=("order_status", lambda status: (status == "Cancelled").mean() * 100),
    )
    fulfillment = delivered.groupby(segment).agg(
        delivered_orders=("order_id", "count"),
        delivered_revenue=("order_value", "sum"),
        avg_delivery_minutes=("delivery_minutes", "mean"),
        avg_customer_rating=("customer_rating", "mean"),
        on_time_rate=("on_time", "mean"),
    )
    summary = totals.join(fulfillment).sort_values("delivered_revenue", ascending=False)
    summary["cancellation_rate"] = summary["cancellation_rate"].round(1)
    summary["avg_delivery_minutes"] = summary["avg_delivery_minutes"].round(1)
    summary["avg_customer_rating"] = summary["avg_customer_rating"].round(2)
    summary["on_time_rate"] = (summary["on_time_rate"] * 100).round(1)
    return summary


def main():
    orders = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    delivered = orders[orders["order_status"] == "Delivered"].copy()
    delivered["on_time"] = delivered["delivery_minutes"] <= delivered["promised_minutes"]

    monthly = (
        delivered.set_index("order_date")
        .resample("MS")
        .agg(revenue=("order_value", "sum"), orders=("order_id", "count"))
    )
    city_performance = summarize_segment(orders, delivered, "city")
    category_performance = summarize_segment(orders, delivered, "restaurant_category")
    channel_performance = summarize_segment(orders, delivered, "acquisition_channel")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, summary in (
        ("city", city_performance),
        ("category", category_performance),
        ("channel", channel_performance),
    ):
        summary.to_csv(OUTPUT_DIR / f"{name}_performance.csv")

    monthly.plot(y="revenue", marker="o", legend=False, figsize=(9, 5), color="#147D75")
    plt.title("Monthly Delivered Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue ($)")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=150)
    plt.close()

    city_performance["delivered_revenue"].sort_values().plot(
        kind="barh", figsize=(8, 5), color="#147D75"
    )
    plt.title("Delivered Revenue by City")
    plt.xlabel("Revenue ($)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "revenue_by_city.png", dpi=150)
    plt.close()

    city_performance["avg_delivery_minutes"].sort_values().plot(
        kind="barh", figsize=(8, 5), color="#D77945"
    )
    plt.title("Average Delivery Time by City")
    plt.xlabel("Minutes")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "delivery_time_by_city.png", dpi=150)
    plt.close()

    city_performance["on_time_rate"].sort_values().plot(
        kind="barh", figsize=(8, 5), color="#3D7890"
    )
    plt.title("On-Time Delivery Rate by City")
    plt.xlabel("On-time orders (%)")
    plt.ylabel("")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "on_time_rate_by_city.png", dpi=150)
    plt.close()

    category_performance["avg_customer_rating"].sort_values().plot(
        kind="barh", figsize=(8, 5), color="#D77945"
    )
    plt.title("Average Customer Rating by Restaurant Category")
    plt.xlabel("Rating (1-5)")
    plt.ylabel("")
    plt.xlim(1, 5)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "rating_by_category.png", dpi=150)
    plt.close()

    channel_performance["cancellation_rate"].sort_values().plot(
        kind="barh", figsize=(8, 5), color="#3D7890"
    )
    plt.title("Cancellation Rate by Acquisition Channel")
    plt.xlabel("Cancelled orders (%)")
    plt.ylabel("")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "cancellation_by_channel.png", dpi=150)
    plt.close()

    cancellation_rate = (orders["order_status"] == "Cancelled").mean() * 100
    on_time_rate = delivered["on_time"].mean() * 100
    print(f"Orders analyzed: {len(orders):,}")
    print(f"Delivered revenue: ${delivered['order_value'].sum():,.2f}")
    print(f"Cancellation rate: {cancellation_rate:.1f}%")
    print(f"On-time delivery rate: {on_time_rate:.1f}%")
    print(f"Average delivery time: {delivered['delivery_minutes'].mean():.1f} minutes")
    print(f"Saved charts and segment metrics to {OUTPUT_DIR}")
    print(city_performance.to_string())
    print("\nPerformance by restaurant category:")
    print(category_performance.to_string())
    print("\nPerformance by acquisition channel:")
    print(channel_performance.to_string())


if __name__ == "__main__":
    main()