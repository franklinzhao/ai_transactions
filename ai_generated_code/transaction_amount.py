# filename: transaction_amount.py

import json

def calculate_grocery_spending(json_file_path, category, start_date, end_date):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Convert dates to comparable integers
    start_date_int = int(start_date)
    end_date_int = int(end_date)
    
    total_spending = 0
    for transaction in data:
        # Convert postedDate to comparable integer
        postedDate_int = int(transaction['postedDate'])
        
        if start_date_int <= postedDate_int <= end_date_int and transaction['mechBackItemCode'] == category:
            total_spending += float(transaction['transactionAmount'])
    
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Total Transaction Amount for {category} in the given period: ${total_spending:.2f}")

# Usage
json_file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
category = 'GROCERY'
start_date = '20221201'  # December 1, 2022
end_date = '20221231'  # December 31, 2022

calculate_grocery_spending(json_file_path, category, start_date, end_date)