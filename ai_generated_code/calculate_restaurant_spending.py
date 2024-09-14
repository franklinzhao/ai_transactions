# filename: calculate_restaurant_spending.py
import json

def calculate_restaurant_spending(data_path):
    total_amount = 0
    start_date = '20220301'
    end_date = '20220331'

    with open(data_path, 'r') as file:
        data = json.load(file)

    for transaction in data:
        posted_date = transaction['postedDate']
        category = transaction['mechBackItemCode']
        amount = float(transaction['transactionAmount'])

        if category == 'RESTAURANT' and start_date <= posted_date <= end_date:
            total_amount += amount

    print(f"Total spending for RESTAURANT from {start_date} to {end_date}: {total_amount}")

calculate_restaurant_spending('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')