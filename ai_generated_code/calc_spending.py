# filename: calc_spending.py
import json

def calc_spending(file_path, category, date_range):
    spent_amount = 0
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    if data['mechBackItemCode'] == category and date_range[0] <= data['postedDate'] <= date_range[1]:
                        spent_amount += float(data['transactionAmount'])
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line}")
                except KeyError:
                    print(f"Skipping line with missing keys: {line}")
    return spent_amount


file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
category = 'RESTAURANT'
date_range = ('20220301', '20220331')

spent_amount = calc_spending(file_path, category, date_range)
print(f'Spending for {category} in {date_range[0][:4]}-{date_range[0][4:6]}: {spent_amount}')