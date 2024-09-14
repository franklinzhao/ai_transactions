# filename: spendings.py
import json
from datetime import datetime

def get_recent_spending_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Filter data by mechBackItemCode equal to GROCERY
    grocery_data = [item for item in data if item['mechBackItemCode'] == 'GROCERY']
    
    # Get the most recent date
    recent_date = max([item['postedDate'] for item in grocery_data])
    recent_date = datetime.strptime(recent_date, '%Y%m%d')
    
    # Get the date 3 months ago
    three_months_ago = recent_date.strftime('%Y%m%d')
    three_months_ago = int(three_months_ago) - 92  # 92 days is approximately 3 months
    
    # Filter data by most recent 3 months
    recent_grocery_data = [item for item in grocery_data if int(item['postedDate']) >= three_months_ago]
    
    # Calculate the total spending
    total_spending = sum([float(item['transactionAmount']) for item in recent_grocery_data if float(item['transactionAmount']) < 0])
    
    return abs(total_spending)

file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
total_spending = get_recent_spending_data(file_path)
print(total_spending)