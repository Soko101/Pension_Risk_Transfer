# -*- coding: utf-8 -*-
"""PRT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_KQbRdvoNmSf1dyUeC_vgOYIAkDwLDZp
"""

import pandas as pd

# Sample data creation for demonstration purposes
data = {
    'Age': [30, 40, 50, 60, 70],
    'MortalityRate': [0.001, 0.002, 0.005, 0.01, 0.02],
    'InterestRate': [0.03, 0.035, 0.04, 0.045, 0.05],
    'Liability': [100000, 150000, 200000, 250000, 300000]
}

df = pd.DataFrame(data)
print("Initial DataFrame:")
print(df)

# Placeholder for ALM modeling
def alm_simulation(interest_rate, liabilities):
    # Simple simulation logic
    assets = liabilities * (1 + interest_rate)
    return assets

df['SimulatedAssets'] = df.apply(lambda row: alm_simulation(row['InterestRate'], row['Liability']), axis=1)
print("\nDataFrame with Simulated Assets:")
print(df)

# Sensitivity analysis
def sensitivity_analysis(rate_variation, liability):
    results = {}
    for rate in rate_variation:
        assets = liability * (1 + rate)
        results[rate] = assets
    return results

rate_variation = [0.03, 0.035, 0.04, 0.045, 0.05]
df['SensitivityAssets'] = df['Liability'].apply(lambda x: sensitivity_analysis(rate_variation, x))

print("\nDataFrame with Sensitivity Analysis:")
print(df)

# Display the sensitivity analysis results in a more readable format
sensitivity_df = pd.DataFrame(df['SensitivityAssets'].tolist(), index=df['Age'])
print("\nSensitivity Analysis Results:")
print(sensitivity_df)

import matplotlib.pyplot as plt
import seaborn as sns

# Visualize mortality rate by age
plt.figure(figsize=(10, 6))
sns.lineplot(x='Age', y='MortalityRate', data=df)
plt.title('Mortality Rate by Age')
plt.xlabel('Age')
plt.ylabel('Mortality Rate')
plt.show()

# Visualize liability by age
plt.figure(figsize=(10, 6))
sns.barplot(x='Age', y='Liability', data=df)
plt.title('Liability by Age')
plt.xlabel('Age')
plt.ylabel('Liability')
plt.show()

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Split data into training and testing sets
X = df[['Age', 'InterestRate']]
y = df['Liability']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict liabilities
y_pred = rf_model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"\nMean Squared Error of the Random Forest Model: {mse}")

# Adding the predicted liabilities to the DataFrame for visualization
df['PredictedLiability'] = rf_model.predict(X)
print("\nDataFrame with Predicted Liabilities:")
print(df)

# Visualize predicted liabilities vs actual liabilities
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Age', y='Liability', data=df, label='Actual Liability')
sns.scatterplot(x='Age', y='PredictedLiability', data=df, label='Predicted Liability', marker='x')
plt.title('Actual vs Predicted Liabilities by Age')
plt.xlabel('Age')
plt.ylabel('Liability')
plt.legend()
plt.show()