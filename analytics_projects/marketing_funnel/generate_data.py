import numpy as np
import pandas as pd

np.random.seed(9)

stages = ['visit', 'signup', 'trial', 'purchase', 'renewal']
steps = {
    'visit': 5000,
    'signup': 1800,
    'trial': 850,
    'purchase': 360,
    'renewal': 120,
}

rows = []
for stage in stages:
    rows.append({'stage': stage, 'count': steps[stage]})

funnel = pd.DataFrame(rows)
out = 'd:/data/analytics_projects/marketing_funnel/funnel_data.csv'
funnel.to_csv(out, index=False)
print(f'Saved funnel data to {out}')
