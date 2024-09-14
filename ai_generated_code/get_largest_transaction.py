# filename: get_largest_transaction.py
import json

def get_largest_transaction(datapath):
    with open(datapath) as f:
        data = json.load(f)
    
    # find the largest transaction amount
    largest_amount = max(d.get('transactionAmount', 0) for d in data)
    print(f"The biggest transactionAmount: {largest_amount}")

get_largest_transaction('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')