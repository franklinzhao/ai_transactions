# filename: calculate_spending.py
import json

def calculate_spending(data_file):
    with open(data_file, 'r') as file:
        data = json.load(file)

    start_date = '20210301'
    end_date = '20210331'
    total_amount = 0

    for transaction in data:
        if transaction['mechBackItemCode'] == 'MORTGAGE PAYMENT' and start_date <= transaction['postedDate'] <= end_date:
            total_amount += float(transaction['transactionAmount'].replace(',', ''))

    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Total Transaction Amount for MORTGAGE PAYMENT in March 2021: ${total_amount:.2f}")

calculate_spending('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')