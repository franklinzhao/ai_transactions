# filename: total_spending.py
import json
from datetime import datetime

def total_spending(datapath):
    with open(datapath, 'r') as file:
        data = json.load(file)

    # Convert 'postedDate' to datetime object for easier comparison
    for transaction in data:
        transaction['postedDate'] = datetime.strptime(transaction['postedDate'], '%Y%m%d')

    # Get the most recent date
    max_date = max(transaction['postedDate'] for transaction in data)

    # Filter data for the most recent 3 months
    recent_data = [transaction for transaction in data if (max_date - transaction['postedDate']).days <= 92]

    # Filter data for 'mechBackItemCode' equal to 'GROCERY'
    grocery_data = [transaction for transaction in recent_data if transaction['mechBackItemCode'] == 'GROCERY']

    # Calculate the total spending
    total_spending = sum(float(transaction['transactionAmount']) for transaction in grocery_data)

    print(total_spending)

total_spending('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')