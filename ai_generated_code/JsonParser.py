# filename: JsonParser.py
import json

datapath = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'

# load json data
with open(datapath) as f:
    data = json.load(f)

# parse the json data and sum spending for mechBackItemCode equal GROCERY for most recent 3 month 
from datetime import datetime

месяц_назад = datetime.now().strftime('%Y%m%d')

месяц_назад = int(месяц_назад)

grocery_spending = 0
dates = set()
for item in data:
    if item['mechBackItemCode'] == 'GROCERY':
        date = int(item['postedDate'])
        dates.add(date)

dates = sorted(list(dates))

if len(dates) >= 3:
    start = dates[-3]
else:
    start = min(dates) if dates else 0

grocery_spending = 0
for item in data:
    if item['mechBackItemCode'] == 'GROCERY' and int(item['postedDate']) >= start:
        grocery_spending += float(item['transactionAmount'])
print(grocery_spending)