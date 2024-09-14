# filename: data_processor.py
import json
from collections import defaultdict
from datetime import datetime, timedelta

def process_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Process data and calculate total spending for each category
    total_spending = defaultdict(float)
    recent_date = datetime.min
    earliest_date = datetime.max
    total_transactions = 0
    for transaction in data:
        if transaction['mechBackItemCode'] == 'GROCERY':
            date = datetime.strptime(transaction['postedDate'], '%Y%m%d')
            recent_date = max(recent_date, date)
            earliest_date = min(earliest_date, date)
            total_transactions += 1
            total_spending[transaction['mechBackItemCode']] += float(transaction['transactionAmount'])

    recent_spending = sum(float(transaction['transactionAmount']) for transaction in data 
                          if transaction['mechBackItemCode'] == 'GROCERY' 
                          and datetime.strptime(transaction['postedDate'], '%Y%m%d') > datetime.now() - timedelta(days=90))

    return total_spending.get('GROCERY', 0), total_transactions, recent_date, earliest_date, recent_spending

# Main function
if __name__ == "__main__":
    file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
    spending, total_transactions, recent_date, earliest_date, recent_spending = process_data(file_path)
    print(f'Total spending for GROCERY in the entire dataset: ${spending:.2f}')
    print(f'Total number of transactions for GROCERY in the entire dataset: {total_transactions}')
    print(f'Most recent transaction date for GROCERY: {recent_date.strftime("%Y-%m-%d")}')
    print(f'Earliest transaction date for GROCERY: {earliest_date.strftime("%Y-%m-%d")}')
    print(f'Total spending for GROCERY in the last 3 months: ${recent_spending:.2f}')