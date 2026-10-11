import numpy as np
import pandas as pd

np.random.seed(42)

regions = ['North', 'South', 'East', 'West']
products = ['Laptop', 'Phone', 'Tablet', 'Headphones']

rows = []
for _ in range(500):
    date = pd.Timestamp('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365), unit='D')
    rows.append({
        'date': date,
        'region': np.random.choice(regions),
        'product': np.random.choice(products),
        'units_sold': np.random.randint(10, 200),
        'unit_price': round(np.random.uniform(50, 1500), 2),
        'discount': round(np.random.uniform(0, 0.3), 2),
    })

df = pd.DataFrame(rows)
df['revenue'] = (df['units_sold'] * df['unit_price']) * (1 - df['discount'])
df['month'] = df['date'].dt.to_period('M').astype(str)

output_path = 'd:/data/analytics_projects/sales_insights/sales_data.csv'
df.to_csv(output_path, index=False)
print(f'Saved sales data to {output_path}')
