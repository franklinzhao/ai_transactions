# filename: get_grocery_spending.py
import json
from datetime import datetime, timedelta

def get_grocery_transactions(data_file_path):
    total_transactions = 0
    total_grocery_transactions = 0
    total_grocery_spending = 0
    with open(data_file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading and trailing whitespace
            if not line:  # Check if the line is empty
                continue
            try:
                line_dict = json.loads(line)
                total_transactions += 1
                print(f"Date: {line_dict['postedDate']}, mechBackItemCode: {line_dict['mechBackItemCode']}, transactionAmount: {line_dict['transactionAmount']}")
                if line_dict['mechBackItemCode'] == 'GROCERY':
                    total_grocery_transactions += 1
                    total_grocery_spending += float(line_dict['transactionAmount'])
            except json.JSONDecodeError:  # Catch any JSON decoding errors
                continue
    print(f"Total transactions: {total_transactions}")
    print(f"Total 'GROCERY' transactions: {total_grocery_transactions}")
    print(f"Total 'GROCERY' spending: {total_grocery_spending}")

get_grocery_transactions('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')