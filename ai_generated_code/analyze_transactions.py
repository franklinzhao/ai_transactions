# filename: analyze_transactions.py
import json

def analyze_transactions(data_file):
    total_amount = 0
    start_date = '20220301'
    end_date = '20220331'

    with open(data_file, 'r') as file:
        for line in file:
            # Remove leading and trailing whitespace from the line
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            try:
                transaction = json.loads(line)

                if transaction['mechBackItemCode'] == 'CREDIT CARD PAYMENT' and start_date <= transaction['postedDate'] <= end_date:
                    total_amount += float(transaction['transactionAmount'])

            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON: {e}")

    return start_date, end_date, total_amount

data_file = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
start_date, end_date, total_amount = analyze_transactions(data_file)

print(f'Start Date: {start_date}')
print(f'End Date: {end_date}')
print(f'Total Spending for CREDIT CARD PAYMENT: {total_amount}')