# Data Analytics Projects

This workspace contains four practical data analytics mini-projects, one combined portfolio dashboard, and one Logitech brand analytics dashboard.

## Projects

1. Sales Insights Dashboard
   - Tracks sales trends, regional performance, and product revenue share.
   - Built with Python, Pandas, NumPy, and Matplotlib.

2. Customer Churn Analysis
   - Predicts churn risk and highlights the main customer drivers.
   - Uses synthetic customer data and logistic regression.

3. Marketing Funnel Analysis
   - Measures campaign performance and conversion rates across funnel stages.
   - Useful for understanding acquisition and retention efficiency.

4. Combined Portfolio Dashboard
   - Brings all three analyses into one interactive Streamlit app.
   - Lets a recruiter or stakeholder quickly review key results.

5. Logitech Analytics Dashboard
   - A branded dashboard for a Logitech-style product, sales, and customer quality analysis.
   - Shows revenue trends, product mix, region impact, and customer satisfaction insights.

6. Delivery Operations Analysis
   - Analyzes delivery revenue, cancellations, speed, and on-time performance across cities.
   - Generates reproducible synthetic data and saves charts and city-level metrics.

## How to run

Install dependencies:

```bash
cd d:\data\analytics_projects
python -m pip install -r requirements.txt
```

Run the individual scripts:

```bash
python sales_insights\dashboard.py
python customer_churn\churn_analysis.py
python marketing_funnel\funnel_analysis.py
cd delivery_operations
python generate_data.py
python analyze_deliveries.py
```

Run the combined dashboard:

```bash
streamlit run portfolio_dashboard.py
```

Run the Logitech dashboard:

```bash
cd logitech_analytics
python generate_data.py
streamlit run dashboard.py
```

Each project generates charts inside its `outputs/` folder when executed.
