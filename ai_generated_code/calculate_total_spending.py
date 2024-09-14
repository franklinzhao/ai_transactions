# filename: calculate_total_spending.py

import json

# define the start and end dates
start_date = '20220301'
end_date = '20220331'

# initialize the total spending amount
total_spending = 0

# load the data from the json file
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as f:
    for line in f:
        try:
            data = json.loads(line.strip())
            #extract desired data
            mechBackItemCode = data['mechBackItemCode']
            transactionAmount = float(data['transactionAmount'])
            postedDate = data['postedDate']

            if mechBackItemCode=='E-TRANSFER' and start_date <= postedDate <= end_date:
                total_spending += abs(transactionAmount)
        except json.JSONDecodeError as e:
            print(f"Skipping line: {line}, reason: {e}")

# print the result
print(f"Total spending for E-TRANSFER in 2022 March: {total_spending}")
print(f"Start date: {start_date}")
print(f"End date: {end_date}")