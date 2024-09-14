# filename: transaction_analysis.py
import json
from datetime import datetime, timedelta

def get_last_posted_date(data):
    last_posted_date = max([datetime.strptime(x['postedDate'], '%Y%m%d') for x in data])
    return last_posted_date

def get_start_date(last_posted_date):
    start_date = last_posted_date - timedelta(days=90)
    return start_date

def get_total_transaction_amount(data, start_date, last_posted_date):
    total_amount = sum([float(x['transactionAmount']) for x in data if x['mechBackItemCode'] == 'GROCERY' and start_date <= datetime.strptime(x['postedDate'], '%Y%m%d') <= last_posted_date])
    return total_amount

def main():
    with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as f:
        data = json.load(f)
    
    last_posted_date = get_last_posted_date(data)
    start_date = get_start_date(last_posted_date)
    total_amount = get_total_transaction_amount(data, start_date, last_posted_date)

    print(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
    print(f"End Date: {last_posted_date.strftime('%Y-%m-%d')}")
    print(f"Total Transaction Amount for GROCERY: {total_amount}")

if __name__ == "__main__":
    main()