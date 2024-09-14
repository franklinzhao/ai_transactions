# filename: transaction_dates.py
import json
from datetime import datetime

def get_earliest_and_latest_transaction_dates(data):
    dates = [datetime.strptime(transaction['postedDate'], '%Y%m%d') for transaction in data]
    earliest_date = min(dates)
    latest_date = max(dates)
    return earliest_date.strftime('%Y-%m-%d'), latest_date.strftime('%Y-%m-%d')

def main():
    with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json') as f:
        data = json.load(f)

    earliest_date, latest_date = get_earliest_and_latest_transaction_dates(data)
    print(f"Earliest transaction date: {earliest_date}")
    print(f"Latest transaction date: {latest_date}")

if __name__ == "__main__":
    main()