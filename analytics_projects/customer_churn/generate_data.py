import numpy as np
import pandas as pd

np.random.seed(7)

n = 1200

df = pd.DataFrame({
    'age': np.random.randint(18, 70, n),
    'tenure_months': np.random.randint(1, 72, n),
    'monthly_spend': np.random.uniform(20, 200, n),
    'support_tickets': np.random.poisson(2, n),
    'contract_type': np.random.choice(['Month-to-Month', 'Annual', 'Biannual'], n),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n),
})

churn_score = (
    0.02 * df['age'] +
    -0.015 * df['tenure_months'] +
    0.03 * (df['monthly_spend'] / 10) +
    0.18 * df['support_tickets']
)

base = 0.2
prob = 1 / (1 + np.exp(-(base - churn_score / 12)))
# Add a few strong churn indicators
for i in range(len(df)):
    if df.loc[i, 'support_tickets'] >= 5:
        prob.iloc[i] += 0.18
    if df.loc[i, 'contract_type'] == 'Month-to-Month':
        prob.iloc[i] += 0.12
    if df.loc[i, 'tenure_months'] <= 6:
        prob.iloc[i] += 0.10

prob = np.clip(prob, 0, 0.95)
df['churned'] = np.random.binomial(1, prob)
df['churned'] = df['churned'].astype(int)

out = 'd:/data/analytics_projects/customer_churn/customer_data.csv'
df.to_csv(out, index=False)
print(f'Saved churn data to {out}')
