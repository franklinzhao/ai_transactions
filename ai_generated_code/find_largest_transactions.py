# filename: find_largest_transactions.py
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Load the data from the JSON file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Filter the data for the last 3 months and find the largest transaction amount by mechBackItemCode
def find_largest_transactions(data):
    # Convert the postedDate to datetime for easy comparison
    for item in data:
        item['postedDate'] = datetime.strptime(item['postedDate'], '%Y%m%d')
    
    # Find the last 3 months
    max_date = max(item['postedDate'] for item in data)
    three_months_ago = max_date - relativedelta(months=3)
    
    # Find the largest transaction amount by mechBackItemCode
    filtered_data = [item for item in data if item['postedDate'] >= three_months_ago and item['postedDate'] <= max_date]
    
    max_amounts = {}
    for item in filtered_data:
        mechBackItemCode = item['mechBackItemCode']
        transactionAmount = float(item['transactionAmount'])
        if mechBackItemCode not in max_amounts:
            max_amounts[mechBackItemCode] = transactionAmount
        else:
            max_amounts[mechBackItemCode] = max(max_amounts[mechBackItemCode], transactionAmount)
    
    return max_amounts

# Run the code
file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
data = load_data(file_path)
max_amounts = find_largest_transactions(data)
for mechBackItemCode, amount in max_amounts.items():
    print(f"{mechBackItemCode}: {amount}")