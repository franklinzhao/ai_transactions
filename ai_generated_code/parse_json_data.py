# filename: parse_json_data.py
import json
from datetime import datetime

def get_recent_grocery_spending(data_path):
    # Load the JSON data from the file
    with open(data_path, 'r') as f:
        data = json.load(f)

    # Sort the data by postedDate in descending order
    sorted_data = sorted(data, key=lambda x: x['postedDate'], reverse=True)

    # Calculate the total spending for the mechBackItemCode equal to 'GROCERY' in the most recent 3 months
    total_spending = 0
    month_count = 0
    current_month = None
    for item in sorted_data:
        posted_date = datetime.strptime(item['postedDate'], '%Y%m%d')
        if item['mechBackItemCode'] == 'GROCERY':
            if current_month is None:
                current_month = posted_date.strftime('%Y%m')
            elif posted_date.strftime('%Y%m') != current_month and month_count < 3:
                month_count += 1
                current_month = posted_date.strftime('%Y%m')
            if month_count <= 3:
                total_spending += float(item['transactionAmount'])

    return total_spending

# Specify the path to the JSON data file
data_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'

# Get the total spending for the recent 3 months
recent_grocery_spending = get_recent_grocery_spending(data_path)

print(f'The total spending for GROCERY in the last 3 months is: {recent_grocery_spending}')