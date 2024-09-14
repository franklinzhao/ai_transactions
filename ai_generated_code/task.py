# filename: task.py
import json
from datetime import datetime

def is_latest_three_month(postedDate):
    today = datetime.now()
    posted_date = datetime.strptime(postedDate, '%Y%m%d')
    diff = (today - posted_date).days
    return diff <= 90

def find_biggest_total_transaction_amount(datapath):
    with open(datapath) as f:
        data = json.load(f)

    transaction_amounts = {}
    for transaction in data:
        postedDate = transaction['postedDate']
        mechBackItemCode = transaction['mechBackItemCode']
        transactionAmount = transaction['transactionAmount']
        print(f'Date: {postedDate}, mechBackItemCode: {mechBackItemCode}, transactionAmount: {transactionAmount}')
        if is_latest_three_month(postedDate):
            if mechBackItemCode in transaction_amounts:
                transaction_amounts[mechBackItemCode].append(float(transactionAmount.replace(',', '')))
            else:
                transaction_amounts[mechBackItemCode] = [float(transactionAmount.replace(',', ''))]

    if not transaction_amounts:
        print(f'mechBackItemCode: , Biggest Total transactionAmount: 0')
    else:
        max_code = max(transaction_amounts, key=lambda k: sum(transaction_amounts[k]))
        print(f'mechBackItemCode: {max_code}, Biggest Total transactionAmount: {sum(transaction_amounts[max_code])}')

find_biggest_total_transaction_amount('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')