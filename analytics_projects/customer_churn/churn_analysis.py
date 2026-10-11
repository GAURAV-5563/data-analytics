import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = 'd:/data/analytics_projects/customer_churn/customer_data.csv'
OUTPUT_DIR = 'd:/data/analytics_projects/customer_churn/outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df = pd.get_dummies(df, columns=['contract_type', 'region'], drop_first=True)

X = df.drop(columns=['churned'])
y = df['churned']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print('Accuracy:', round(accuracy_score(y_test, y_pred), 3))
print(classification_report(y_test, y_pred))

coeffs = pd.DataFrame({
    'feature': X.columns,
    'coef': model.coef_[0]
}).sort_values('coef', key=lambda s: s.abs(), ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(coeffs['feature'], coeffs['coef'], color='steelblue')
plt.title('Feature Importance (Logistic Regression Coefficients)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature_importance.png'))
plt.close()

print('Saved model analysis output to', OUTPUT_DIR)
