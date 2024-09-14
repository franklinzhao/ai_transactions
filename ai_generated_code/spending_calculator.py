# filename: spending_calculator.py
import json

def calculate_spending(data_path, category, start_date, end_date):
    total_spending = 0
    total_records = 0
    total_transactions = 0
    with open(data_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                total_records += 1
                if 'mechBackItemCode' in data and data['mechBackItemCode'] == category:
                    total_transactions += 1
                    if start_date <= data['postedDate'] <= end_date and data['transactionAmount'] is not None:
                        total_spending += float(data['transactionAmount'])
            except json.JSONDecodeError:
                continue
    print(f"Total records: {total_records}")
    print(f"Total transactions for {category}: {total_transactions}")
    print(f"Total spending for {category} from {start_date} to {end_date}: {total_spending}")

data_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
category = 'RESTAURANT'
start_date = '20220601'
end_date = '20220630'

calculate_spending(data_path, category, start_date, end_date)