import pandas as pd
import sqlite3
import os

# Load CSV
df = pd.read_csv('customer_shopping_behavior.csv')

# Transformations
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

labels = ['Young Adult', 'Adult', 'Middle-Age', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

df.to_csv("final_data.csv", index=False)

# Create fresh DB
conn = sqlite3.connect('shopping.db')

df.to_sql('customer_shopping_behavior', conn, if_exists='replace', index=False)

conn.close()

print("Database created at:", os.getcwd())
