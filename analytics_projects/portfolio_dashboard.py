import os

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title='Data Analytics Portfolio Dashboard',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #111827 35%, #0b1120 100%);
            color: #e2e8f0;
        }
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3, h4 {
            color: #f8fafc !important;
        }
        .metric-container {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
        }
        .kpi-label {
            color: #94a3b8;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .kpi-value {
            color: #f8fafc;
            font-size: 1.7rem;
            font-weight: 700;
            margin-top: 0.2rem;
        }
        .summary-card {
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid rgba(148, 163, 184, 0.2);
            padding: 1rem 1.1rem;
            border-radius: 14px;
            margin-top: 0.8rem;
        }
        .summary-card strong {
            color: #f8fafc;
        }
        .summary-card span {
            color: #cbd5e1;
        }
        .stDataFrame {
            background: rgba(15, 23, 42, 0.6);
            border-radius: 12px;
        }
        .stMetric {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 14px;
            padding: 0.8rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALES_PATH = os.path.join(BASE_DIR, 'sales_insights', 'sales_data.csv')
CHURN_PATH = os.path.join(BASE_DIR, 'customer_churn', 'customer_data.csv')
FUNNEL_PATH = os.path.join(BASE_DIR, 'marketing_funnel', 'funnel_data.csv')


@st.cache_data
def load_sales_data():
    df = pd.read_csv(SALES_PATH)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    return df


@st.cache_data
def load_churn_data():
    return pd.read_csv(CHURN_PATH)


@st.cache_data
def load_funnel_data():
    return pd.read_csv(FUNNEL_PATH)


st.title('Data Analytics Portfolio Dashboard')
st.caption('Sales performance, churn analysis, and marketing funnel insights')

sales_df = load_sales_data()
churn_df = load_churn_data()
funnel_df = load_funnel_data()

sales_total = sales_df['revenue'].sum()
regional_best = sales_df.groupby('region')['revenue'].sum().sort_values(ascending=False).head(1)
product_best = sales_df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(1)
churn_rate = churn_df['churned'].mean() * 100
avg_order_value = sales_df['revenue'].mean()

st.markdown(
    """
    <div class='summary-card'>
        <strong>Portfolio Summary:</strong>
        <span>Sales performance is lead-driven by the West region, while churn risk is concentrated in customer segments with higher support demand and shorter tenure.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Revenue', f'${sales_total:,.0f}')
col2.metric('Top Region', regional_best.index[0])
col3.metric('Top Product', product_best.index[0])
col4.metric('Churn Rate', f'{churn_rate:.1f}%')

st.markdown('---')
st.subheader('Business Overview')
left_col, right_col = st.columns(2)

with left_col:
    monthly_sales = sales_df.groupby('month', as_index=False)['revenue'].sum().sort_values('month')
    fig, ax = plt.subplots(figsize=(9, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.plot(monthly_sales['month'], monthly_sales['revenue'], marker='o', color='#7dd3fc', linewidth=2.8)
    ax.set_title('Monthly Revenue Trend', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Month', color='#cbd5e1')
    ax.set_ylabel('Revenue', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1', rotation=45)
    ax.tick_params(axis='y', colors='#cbd5e1')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#334155')
    fig.tight_layout()
    st.pyplot(fig)

with right_col:
    region_sales = sales_df.groupby('region', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
    fig, ax = plt.subplots(figsize=(7.5, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(region_sales['region'], region_sales['revenue'], color=['#38bdf8', '#a78bfa', '#f59e0b', '#f472b6'])
    ax.set_title('Revenue by Region', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Region', color='#cbd5e1')
    ax.set_ylabel('Revenue', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1')
    ax.tick_params(axis='y', colors='#cbd5e1')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Customer Churn Insights')
churn_tab1, churn_tab2 = st.columns(2)
with churn_tab1:
    churn_summary = churn_df.groupby('contract_type')['churned'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(churn_summary['contract_type'], churn_summary['churned'] * 100, color=['#f87171', '#fbbf24', '#34d399'])
    ax.set_title('Churn Rate by Contract Type', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Contract Type', color='#cbd5e1')
    ax.set_ylabel('Churn %', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1')
    ax.tick_params(axis='y', colors='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

with churn_tab2:
    avg_spend_by_outcome = churn_df.groupby('churned')['monthly_spend'].mean().reset_index()
    avg_spend_by_outcome['outcome'] = ['No Churn', 'Churn']
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.bar(avg_spend_by_outcome['outcome'], avg_spend_by_outcome['monthly_spend'], color='#60a5fa')
    ax.set_title('Average Monthly Spend by Outcome', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Outcome', color='#cbd5e1')
    ax.set_ylabel('Average Spend', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1')
    ax.tick_params(axis='y', colors='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

st.subheader('Marketing Funnel Performance')
conversion_rates = [100.0]
for i in range(1, len(funnel_df)):
    rate = (funnel_df.loc[i, 'count'] / funnel_df.loc[i - 1, 'count']) * 100
    conversion_rates.append(round(rate, 2))

funnel_df['conversion_rate'] = conversion_rates

funnel_chart, table = st.columns([2, 1])
with funnel_chart:
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.plot(funnel_df['stage'], funnel_df['count'], marker='o', linewidth=2.8, color='#4ade80')
    ax.set_title('Marketing Funnel', color='#f8fafc', fontsize=16)
    ax.set_xlabel('Stage', color='#cbd5e1')
    ax.set_ylabel('Users', color='#cbd5e1')
    ax.tick_params(axis='x', colors='#cbd5e1', rotation=20)
    ax.tick_params(axis='y', colors='#cbd5e1')
    fig.tight_layout()
    st.pyplot(fig)

with table:
    st.dataframe(
        funnel_df[['stage', 'count', 'conversion_rate']].rename(columns={'conversion_rate': 'Conversion %'}),
        hide_index=True,
        use_container_width=True,
    )

st.markdown('---')
st.subheader('Key Takeaways')
st.markdown(
    f"""
    - Revenue is strongest in the top-performing region, with a clear monthly trend signal.
    - Contract type and customer support activity are key churn drivers in the dataset.
    - The funnel shows a high drop-off during the shift from awareness to onboarding.
    - Average order value is approximately ${avg_order_value:,.0f} based on the synthetic revenue data.
    """,
    unsafe_allow_html=False,
)
