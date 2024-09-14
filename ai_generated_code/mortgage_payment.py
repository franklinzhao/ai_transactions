# filename: mortgage_payment.py
import json

def total_spending_mortgage_payment(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        
    start_date = '20210301'
    end_date = '20210331'
    total_spending = 0
    
    for transaction in data:
        if start_date <= transaction['postedDate'] <= end_date and transaction['mechBackItemCode'] == 'MORTGAGE PAYMENT':
            total_spending += float(transaction['transactionAmount'])
            
    return total_spending, start_date, end_date

json_file = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
total_spending, start_date, end_date = total_spending_mortgage_payment(json_file)

print(f'Total spending for MORTGAGE PAYMENT in 2021 March: {total_spending}')
print(f'Date range: {start_date} - {end_date}')