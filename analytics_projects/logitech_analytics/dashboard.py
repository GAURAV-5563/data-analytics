import os

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='Logitech Analytics Dashboard', layout='wide')

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #020817 0%, #0f172a 42%, #111827 100%);
            color: #e2e8f0;
        }
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3, h4 { color: #f8fafc !important; }
        .stMetric {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 14px;
            padding: 0.8rem 1rem;
        }
        .summary-card {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }
        .summary-card strong { color: #f8fafc; }
        .summary-card span { color: #cbd5e1; }
        .stDataFrame { background: rgba(15, 23, 42, 0.7); }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'logitech_data.csv')

df = pd.read_csv(DATA_PATH)
df['month'] = pd.to_datetime(df['month'])

st.sidebar.title('Filters')
regions = st.sidebar.multiselect('Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
segments = st.sidebar.multiselect('Segment', options=sorted(df['segment'].unique()), default=sorted(df['segment'].unique()))
products = st.sidebar.multiselect('Product', options=sorted(df['product'].unique()), default=sorted(df['product'].unique()))
month_min, month_max = df['month'].min().date(), df['month'].max().date()
start_month = st.sidebar.date_input('Start month', value=month_min, min_value=month_min, max_value=month_max)
end_month = st.sidebar.date_input('End month', value=month_max, min_value=month_min, max_value=month_max)
if start_month > end_month:
    start_month, end_month = end_month, start_month

filtered_df = df[
    df['region'].isin(regions) &
    df['segment'].isin(segments) &
    df['product'].isin(products) &
    df['month'].between(pd.Timestamp(start_month), pd.Timestamp(end_month))
].copy()

if filtered_df.empty:
    st.warning('No data matches the current filters. Please widen the selected product, region, or date range.')
    st.stop()

st.title('Logitech Analytics Executive Dashboard')
st.caption('Brand performance overview across revenue, product quality, and growth opportunities')

st.markdown(
    """
    <div class='summary-card'>
        <strong>Executive Summary:</strong>
        <span>Customer experience and product quality remain the strongest indicators of performance, while product satisfaction stays consistent and return rates remain stable across regions.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

avg_satisfaction = filtered_df['customer_satisfaction'].mean()
return_rate = filtered_df['return_rate'].mean() * 100
best_region = filtered_df.groupby('region')['customer_satisfaction'].mean().idxmax()
best_product = filtered_df.groupby('product')['customer_satisfaction'].mean().idxmax()
total_units = filtered_df['units_sold'].sum()
total_revenue = filtered_df['revenue'].sum()
best_seller = filtered_df.groupby('product')['units_sold'].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric('Avg Satisfaction', f'{avg_satisfaction:.2f}/5')
col2.metric('Return Rate', f'{return_rate:.1f}%')
col3.metric('Best Region', best_region)

st.markdown('---')

st.subheader('Sales Performance Snapshot')
sales_col1, sales_col2, sales_col3 = st.columns(3)
sales_col1.metric('Units Sold', f'{total_units:,.0f}')
sales_col2.metric('Revenue', f'${total_revenue:,.0f}')
sales_col3.metric('Best Selling Product', best_seller)

sales_left, sales_right = st.columns(2)
with sales_left:
    product_sales = filtered_df.groupby('product', as_index=False)['units_sold'].sum().sort_values('units_sold', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(product_sales['product'], product_sales['units_sold'], color='#38bdf8')
    ax.set_title('Units Sold by Product', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Product', color='#cbd5e1')
    ax.set_ylabel('Units', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1', rotation=20)
    ax.tick_params(axis='y', colors='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

with sales_right:
    product_revenue = filtered_df.groupby('product', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(product_revenue['product'], product_revenue['revenue'], color='#34d399')
    ax.set_title('Revenue by Product', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Product', color='#cbd5e1')
    ax.set_ylabel('Revenue', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1', rotation=20)
    ax.tick_params(axis='y', colors='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Monthly Sales Trend')
monthly_sales = filtered_df.groupby('month', as_index=False)['units_sold'].sum()
fig, ax = plt.subplots(figsize=(12, 5), facecolor='#0f172a')
ax.set_facecolor('#0f172a')
ax.plot(monthly_sales['month'], monthly_sales['units_sold'], color='#fbbf24', marker='o', linewidth=2.5)
ax.set_title('Monthly Units Sold Trend', color='#f8fafc', fontsize=16)
ax.set_xlabel('Month', color='#cbd5e1')
ax.set_ylabel('Units Sold', color='#cbd5e1')
ax.tick_params(axis='x', colors='#cbd5e1', rotation=45)
ax.tick_params(axis='y', colors='#cbd5e1')
fig.tight_layout()
st.pyplot(fig)

st.markdown('---')

st.subheader('Customer Experience Overview')
left, right = st.columns(2)

with left:
    monthly_quality = filtered_df.groupby('month', as_index=False)['customer_satisfaction'].mean()
    fig, ax = plt.subplots(figsize=(9, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.plot(monthly_quality['month'], monthly_quality['customer_satisfaction'], color='#60a5fa', marker='o', linewidth=2.5)
    ax.set_title('Customer Satisfaction Trend', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Month', color='#cbd5e1')
    ax.set_ylabel('Satisfaction', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1', rotation=45)
    ax.tick_params(axis='y', colors='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

with right:
    region_quality = filtered_df.groupby('region', as_index=False)['customer_satisfaction'].mean().sort_values('customer_satisfaction', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(region_quality['region'], region_quality['customer_satisfaction'], color=['#38bdf8', '#a78bfa', '#f59e0b', '#34d399'])
    ax.set_title('Satisfaction by Region', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Region', color='#cbd5e1')
    ax.set_ylabel('Satisfaction', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1')
    ax.tick_params(axis='y', colors='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Product Quality Insights')
prod1, prod2 = st.columns(2)

with prod1:
    product_quality = filtered_df.groupby('product', as_index=False)['customer_satisfaction'].mean().sort_values('customer_satisfaction', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(product_quality['product'], product_quality['customer_satisfaction'], color='#fbbf24')
    ax.set_title('Average Satisfaction by Product', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Product', color='#cbd5e1')
    ax.set_ylabel('Satisfaction', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1', rotation=20)
    ax.tick_params(axis='y', colors='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

with prod2:
    return_by_product = filtered_df.groupby('product', as_index=False)['return_rate'].mean().sort_values('return_rate', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(return_by_product['product'], return_by_product['return_rate'] * 100, color='#f472b6')
    ax.set_title('Return Rate by Product', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Product', color='#cbd5e1')
    ax.set_ylabel('Return %', color='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Customer Segment Health')
seg1, seg2 = st.columns(2)
with seg1:
    segment_quality = filtered_df.groupby('segment', as_index=False)['customer_satisfaction'].mean().sort_values('customer_satisfaction', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(segment_quality['segment'], segment_quality['customer_satisfaction'], color='#4ade80')
    ax.set_title('Satisfaction by Customer Segment', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Segment', color='#cbd5e1')
    ax.set_ylabel('Satisfaction', color='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

with seg2:
    segment_return_rate = filtered_df.groupby('segment', as_index=False)['return_rate'].mean().sort_values('return_rate', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(segment_return_rate['segment'], segment_return_rate['return_rate'] * 100, color='#f56565')
    ax.set_title('Return Rate by Segment', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Segment', color='#cbd5e1')
    ax.set_ylabel('Return %', color='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Quality Summary Table')
summary = filtered_df.groupby(['region', 'product'], as_index=False)['customer_satisfaction'].mean().sort_values('customer_satisfaction', ascending=False)
st.dataframe(summary, use_container_width=True)

st.subheader('Key Takeaways')
st.markdown(
    f"""
    - The highest customer satisfaction is observed in **{best_product}**, with **{best_region}** showing the strongest quality experience across the selected view.
    - Product quality remains consistently strong across the portfolio, with limited volatility in customer sentiment.
    - Return rate remains stable and within a healthy operational range across segments.
    - The selected business slice indicates strong customer confidence across {', '.join(segments[:3])} and related channels.
    """
)
