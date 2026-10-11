import pandas as pd
import numpy as np

np.random.seed(42)

months = pd.date_range('2024-01-01', '2026-10-01', freq='MS')
regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'India']
products = ['Gaming Mouse', 'Mechanical Keyboard', 'Wireless Headset', 'Webcam', 'USB Hub']
segments = ['Consumer', 'Business', 'Creator', 'Gaming']

rows = []
for month in months:
    for region in regions:
        for product in products:
            for segment in segments:
                units = int(np.random.randint(60, 500))
                unit_price = {
                    'Gaming Mouse': 79,
                    'Mechanical Keyboard': 129,
                    'Wireless Headset': 149,
                    'Webcam': 109,
                    'USB Hub': 49,
                }[product]
                discount = np.random.uniform(0.05, 0.25)
                revenue = units * unit_price * (1 - discount)
                satisfaction = np.random.uniform(4.1, 4.9)
                return_rate = np.random.uniform(0.02, 0.12)
                rows.append({
                    'month': month,
                    'region': region,
                    'product': product,
                    'segment': segment,
                    'units_sold': units,
                    'unit_price': unit_price,
                    'discount': round(discount, 3),
                    'revenue': round(revenue, 2),
                    'customer_satisfaction': round(satisfaction, 2),
                    'return_rate': round(return_rate, 3),
                })

out = pd.DataFrame(rows)
out.to_csv('d:/data/analytics_projects/logitech_analytics/logitech_data.csv', index=False)
print('Logitech data generated successfully.')
