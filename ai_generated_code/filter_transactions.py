# filename: filter_transactions.py
import json

# Load the JSON data file
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as f:
    data = json.load(f)

# Define the parameters for the period
start_date = '20220301'
end_date = '20220331'

# Initialize total transaction amount
total_amount = 0.0

# Calculate the total transaction amount for CHEQUE DEPOSIT
for transaction in data:
    if start_date <= transaction['postedDate'] <= end_date and transaction['mechBackItemCode'] == 'CHEQUE DEPOSIT':
        total_amount += float(transaction['transactionAmount'])

# Print the result
print(f"Total spending for CHEQUE DEPOSIT from {start_date} to {end_date}: ${total_amount:.2f}")