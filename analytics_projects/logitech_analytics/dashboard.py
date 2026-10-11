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
        .stApp { background: linear-gradient(135deg, #0f172a, #111827 55%, #1e293b); }
        h1, h2, h3, h4 { color: white !important; }
        .stMetric { background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(148,163,184,0.2); border-radius: 12px; }
        .stDataFrame { background: rgba(15, 23, 42, 0.7); }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'logitech_data.csv')

df = pd.read_csv(DATA_PATH)
df['month'] = pd.to_datetime(df['month'])

total_revenue = df['revenue'].sum()
total_units = df['units_sold'].sum()
avg_satisfaction = df['customer_satisfaction'].mean()
return_rate = df['return_rate'].mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Revenue', f'${total_revenue:,.0f}')
col2.metric('Units Sold', f'{total_units:,}')
col3.metric('Avg Satisfaction', f'{avg_satisfaction:.2f}/5')
col4.metric('Return Rate', f'{return_rate:.1f}%')

st.markdown('---')

st.subheader('Business Overview')
left, right = st.columns(2)

with left:
    monthly = df.groupby('month', as_index=False)['revenue'].sum()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly['month'], monthly['revenue'], color='#60a5fa', marker='o')
    ax.set_title('Monthly Revenue Trend')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue')
    fig.tight_layout()
    st.pyplot(fig)

with right:
    region_sales = df.groupby('region', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(region_sales['region'], region_sales['revenue'], color=['#38bdf8', '#a78bfa', '#f59e0b', '#34d399'])
    ax.set_title('Revenue by Region')
    ax.set_xlabel('Region')
    ax.set_ylabel('Revenue')
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Product Performance')
prod1, prod2 = st.columns(2)

with prod1:
    product_revenue = df.groupby('product', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(product_revenue['product'], product_revenue['revenue'], color='#fbbf24')
    ax.set_title('Revenue by Product')
    ax.set_xlabel('Product')
    ax.set_ylabel('Revenue')
    fig.tight_layout()
    st.pyplot(fig)

with prod2:
    product_units = df.groupby('product', as_index=False)['units_sold'].sum().sort_values('units_sold', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(product_units['units_sold'], labels=product_units['product'], autopct='%1.1f%%', startangle=90)
    ax.set_title('Units Sold Share by Product')
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Customer & Quality Insights')
seg1, seg2 = st.columns(2)
with seg1:
    segment_sales = df.groupby('segment', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(segment_sales['segment'], segment_sales['revenue'], color='#4ade80')
    ax.set_title('Revenue by Customer Segment')
    ax.set_xlabel('Segment')
    ax.set_ylabel('Revenue')
    fig.tight_layout()
    st.pyplot(fig)

with seg2:
    quality = df.groupby('product', as_index=False)['customer_satisfaction'].mean().sort_values('customer_satisfaction', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(quality['product'], quality['customer_satisfaction'], color='#f472b6')
    ax.set_title('Average Satisfaction by Product')
    ax.set_xlabel('Product')
    ax.set_ylabel('Satisfaction')
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Key Takeaways')
st.markdown(
    """
    - Logitech’s strongest revenue contribution comes from premium accessories and gaming-related products.
    - Asia Pacific and North America are the biggest growth markets in the synthetic dataset.
    - Consumer and gaming segments lead the revenue mix.
    - Satisfaction remains above 4.0 across each product line, while returns remain within a healthy range.
    """
)
