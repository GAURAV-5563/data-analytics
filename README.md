# Data Analytics Portfolio

A collection of data analytics projects covering sales performance, customer churn, marketing funnel conversion, and product quality.

## Live portfolio

Visit the [Data Analytics Portfolio site](https://gaurav-5563.github.io/data-analytics/) to browse the project descriptions and chart previews.

The website is a static GitHub Pages site. The Python dashboards below are source code and require Streamlit to run interactively.

## Projects

- [Sales Insights](./analytics_projects/sales_insights/) — revenue trends, regional performance, and product contribution.
- [Customer Churn Analysis](./analytics_projects/customer_churn/) — churn patterns and customer risk signals.
- [Marketing Funnel](./analytics_projects/marketing_funnel/) — conversion through visits, signups, trials, purchases, and renewals.
- [Logitech Analytics](./analytics_projects/logitech_analytics/) — product sales, customer satisfaction, and returns.
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
