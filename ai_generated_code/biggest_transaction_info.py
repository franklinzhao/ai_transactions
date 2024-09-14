# filename: biggest_transaction_info.py
import json

# Load the data from the JSON file
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as file:
    data = json.load(file)

# Find the biggest transaction amount and its info
if data:
    biggest_transaction_amount = max(data, key=lambda x: float(x.get('transactionAmount', '0').replace(',', '')))
    print("The biggest transaction amount is: ", biggest_transaction_amount.get('transactionAmount'))
    print("Category: ", biggest_transaction_amount.get('category'))
    print("Posted Date: ", biggest_transaction_amount.get('posteddate'))
else:
    print("No transactions found")