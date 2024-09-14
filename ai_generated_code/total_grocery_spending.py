# filename: total_grocery_spending.py

import json
from datetime import datetime

def total_grocery_spending(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Calculate the total spending for mechBackItemCode equal to GROCERY
    total_spending = 0
    for item in data:
        if item['mechBackItemCode'] == 'GROCERY':
            print(f"Transaction Amount: {item['transactionAmount']}, Posted Date: {item['postedDate']}")
            total_spending += float(item['transactionAmount'])

    return total_spending

file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
print(total_grocery_spending(file_path))