# filename: sum_transactions.py

import json

def sum_transactions(file_path, start_date, end_date, category):
    total_amount = 0
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    if start_date <= data['postedDate'] <= end_date and data['mechBackItemCode'] == category:
                        total_amount += float(data['transactionAmount'])
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {line}")
    return total_amount

file_path = "/home/sagemaker-user/ai_transactions/data/data_generated100k.json"
start_date = "20210301"
end_date = "20210331"
category = "MORTGAGE PAYMENT"

total_amount = sum_transactions(file_path, start_date, end_date, category)
print("Total spending for {} in 2021 March: {}".format(category, total_amount))
print("Date range: {} - {}".format(start_date, end_date))