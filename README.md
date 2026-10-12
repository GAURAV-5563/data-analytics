# Data Analytics Portfolio

A collection of data analytics projects covering sales performance, customer churn, marketing funnel conversion, product quality, and delivery operations.

## Live Logitech dashboard

Open the [Logitech Analytics Dashboard](https://gaurav-5563.github.io/data-analytics/) for interactive product, regional, customer satisfaction, and returns analysis.

The live dashboard is hosted on GitHub Pages and reads the Logitech project CSV in your browser. A separate Streamlit implementation is also available in the repository.

## Projects

- [Sales Insights](./analytics_projects/sales_insights/) — revenue trends, regional performance, and product contribution.
- [Customer Churn Analysis](./analytics_projects/customer_churn/) — churn patterns and customer risk signals.
- [Marketing Funnel](./analytics_projects/marketing_funnel/) — conversion through visits, signups, trials, purchases, and renewals.
- [Logitech Analytics](./analytics_projects/logitech_analytics/) — product sales, customer satisfaction, and returns.
- [Delivery Operations Analysis](./analytics_projects/delivery_operations/) — delivery revenue, cancellation rates, and city-level fulfillment performance.
- [Combined Portfolio Dashboard](./analytics_projects/portfolio_dashboard.py) — a Streamlit dashboard combining sales, churn, and funnel insights.

## Run the combined dashboard locally

```bash
cd analytics_projects
python -m pip install -r requirements.txt
streamlit run portfolio_dashboard.py
```

To run the Logitech dashboard instead:

```bash
cd analytics_projects/logitech_analytics
streamlit run dashboard.py
```
