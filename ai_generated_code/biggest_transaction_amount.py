# filename: biggest_transaction_amount.py

import json
import pandas as pd
from datetime import datetime, timedelta

# Load the data from the JSON file
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json') as f:
    data = json.load(f)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Convert the transactionAmount to float and postedDate to datetime
df['transactionAmount'] = df['transactionAmount'].astype(float)
df['postedDate'] = pd.to_datetime(df['postedDate'], format='%Y%m%d')

# Find the latest 3 months
max_date = df['postedDate'].max()
three_months_ago = max_date - pd.DateOffset(months=3)

# Filter the data to the latest 3 months
df_latest_3_months = df[df['postedDate'] >= three_months_ago]

# Group the data by mechBackItemCode and find the max transactionAmount
biggest_transactions = df_latest_3_months.groupby('mechBackItemCode')['transactionAmount'].max().reset_index()

# Sort the biggest transactions in descending order
biggest_transactions = biggest_transactions.sort_values(by='transactionAmount', ascending=False)

# Print the biggest transactionAmount by mechBackItemCode
print(biggest_transactions)