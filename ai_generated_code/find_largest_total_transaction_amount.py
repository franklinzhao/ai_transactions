# filename: find_largest_total_transaction_amount.py

import json
from datetime import datetime, timedelta

# Load the JSON data
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as file:
    data = json.load(file)

# Find the last postedDate
last_posted_date = max(datetime.strptime(transaction['postedDate'], '%Y%m%d') for transaction in data)
three_months_ago_date = last_posted_date - timedelta(days=90)

# Filter data for the last 3 months
data_last_3_months = [transaction for transaction in data if datetime.strptime(transaction['postedDate'], '%Y%m%d') >= three_months_ago_date]

# Group the data by mechBackItemCode and calculate total transactionAmount
total_amounts = {}
for transaction in data_last_3_months:
    mech_back_item_code = transaction['mechBackItemCode']
    transaction_amount = float(transaction['transactionAmount'])
    if mech_back_item_code in total_amounts:
        total_amounts[mech_back_item_code] += transaction_amount
    else:
        total_amounts[mech_back_item_code] = transaction_amount

# Find the mechBackItemCode with the biggest total transactionAmount
biggest_total_amount_item_code = max(total_amounts, key=total_amounts.get)
biggest_total_amount = total_amounts[biggest_total_amount_item_code]

# Print the result
print(f'The biggest total transactionAmount by mechBackItemCode for 3 month period ended at the last postedDate is:')
print(f'mechBackItemCode: {biggest_total_amount_item_code}, Total Amount: {biggest_total_amount}')