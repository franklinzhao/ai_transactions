# filename: calculate_spendding.py
import json
from datetime import datetime

def parse_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def calculate_spending(data):
    total_spending = 0
    recent_dates = set()
    for item in data:
        posted_date = datetime.strptime(item['postedDate'], '%Y%m%d')
        recent_dates.add(posted_date)
    recent_dates = sorted(recent_dates)[-90:]  # get the last 3 months
    
    for item in data:
        posted_date = datetime.strptime(item['postedDate'], '%Y%m%d')
        if posted_date in recent_dates and item['mechBackItemCode'] == 'GROCERY':
            total_spending += float(item['transactionAmount'])
    return total_spending

def main():
    file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
    data = parse_json_file(file_path)
    spending = calculate_spending(data)
    print(f'Total spending for GROCERY is {spending}')

if __name__ == '__main__':
    main()