# filename: grocery_spending.py
import json
from datetime import datetime, timedelta

# Load JSON data
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as f:
    data = json.load(f)

# Convert postedDate to datetime and calculate total transaction amount for 'GROCERY' for the last 3 months
max_date = datetime.strptime('1970-01-01', '%Y-%m-%d')
for transaction in data:
    transaction_date = datetime.strptime(transaction['postedDate'], '%Y%m%d')
    if transaction_date > max_date:
        max_date = transaction_date

start_date = max_date - timedelta(days=90)
total_amount = 0
for transaction in data:
    transaction_date = datetime.strptime(transaction['postedDate'], '%Y%m%d')
    if transaction['mechBackItemCode'] == 'GROCERY' and start_date <= transaction_date <= max_date:
        total_amount += float(transaction['transactionAmount'])

print(f'Total spending for GROCERY for the 3 month period from {start_date.strftime("%Y-%m-%d")} to {max_date.strftime("%Y-%m-%d")}: {total_amount}')