import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATA_PATH = 'd:/data/analytics_projects/sales_insights/sales_data.csv'
OUTPUT_DIR = 'd:/data/analytics_projects/sales_insights/outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

df['month'] = df['date'].dt.to_period('M').astype(str)
monthly_sales = df.groupby('month', as_index=False)['revenue'].sum().sort_values('month')

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales['month'], monthly_sales['revenue'], marker='o')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'monthly_revenue.png'))
plt.close()

region_sales = df.groupby('region', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
plt.figure(figsize=(8, 6))
plt.bar(region_sales['region'], region_sales['revenue'], color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])
plt.title('Revenue by Region')
plt.xlabel('Region')
plt.ylabel('Revenue')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'revenue_by_region.png'))
plt.close()

product_sales = df.groupby('product', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
plt.figure(figsize=(8, 6))
plt.pie(product_sales['revenue'], labels=product_sales['product'], autopct='%1.1f%%')
plt.title('Revenue Contribution by Product')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'revenue_by_product.png'))
plt.close()

print('Saved charts to', OUTPUT_DIR)
