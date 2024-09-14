# filename: calculate_total_spending_december2023.py
import json

# Function to calculate the total spending in a given time period
def calculate_total_spending(data, start_date, end_date):
    total_spending = 0
    for transaction in data:
        posted_date = transaction['postedDate']
        if start_date <= posted_date <= end_date:
            total_spending += float(transaction['transactionAmount'])
    return total_spending

# Read the data from the json file
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as f:
    data = json.load(f)

# Calculate the total spending in December 2023
start_date = '20231201'
end_date = '20231231'
total_spending = calculate_total_spending(data, start_date, end_date)

# Print the result
print(f'The total spending from {start_date} to {end_date} is: {total_spending}')