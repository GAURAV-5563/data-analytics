import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATA_PATH = 'd:/data/analytics_projects/marketing_funnel/funnel_data.csv'
OUTPUT_DIR = 'd:/data/analytics_projects/marketing_funnel/outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

conversion_rates = [100.0]
for i in range(1, len(df)):
    rate = (df.loc[i, 'count'] / df.loc[i - 1, 'count']) * 100
    conversion_rates.append(round(rate, 2))

df['conversion_rate'] = conversion_rates

plt.figure(figsize=(8, 6))
plt.plot(df['stage'], df['count'], marker='o', linewidth=2.5)
plt.title('Marketing Funnel')
plt.xlabel('Stage')
plt.ylabel('Users')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'funnel.png'))
plt.close()

plt.figure(figsize=(8, 6))
plt.bar(df['stage'], df['conversion_rate'], color='seagreen')
plt.title('Conversion Rate by Stage')
plt.xlabel('Stage')
plt.ylabel('Conversion %')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'conversion_rate.png'))
plt.close()

print('Saved funnel charts to', OUTPUT_DIR)
print(df[['stage', 'count', 'conversion_rate']].to_string(index=False))
