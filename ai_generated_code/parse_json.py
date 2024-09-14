# filename: parse_json.py
import json

# Function to calculate total transaction amount
def calculate_total_amount(data, start_date, end_date, category):
    total_amount = 0
    for transaction in data:
        if transaction['postedDate'] >= start_date and transaction['postedDate'] <= end_date and transaction['mechBackItemCode'] == category:
            total_amount += float(transaction['transactionAmount'])
    return total_amount

# Load JSON data
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json') as f:
    data = json.load(f)

# Define the date range and category
start_date = '20220301'
end_date = '20220331'
category = 'RESTAURANT'

# Calculate the total transaction amount
total_amount = calculate_total_amount(data, start_date, end_date, category)

# Print the result
print("Total spending for RESTAURANT from 2022-03-01 to 2022-03-31 is: ", total_amount)