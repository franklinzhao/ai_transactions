# filename: calculate_grocery_spending.py
import json

def calculate_grocery_spending(datapath):
    with open(datapath, 'r') as f:
        data = json.load(f)
    
    grocery_spending = 0
    start_date = '20221201'
    end_date = '20221231'
    
    for transaction in data:
        if transaction['postedDate'] >= start_date and transaction['postedDate'] <= end_date:
            if transaction['mechBackItemCode'] == 'GROCERY':
                grocery_spending += float(transaction['transactionAmount'])
    
    print(f'Total spending for GROCERY from {start_date} to {end_date} is: {grocery_spending}')

calculate_grocery_spending('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')