# filename: filter_data.py
import json

def find_most_recent_date(data):
    most_recent_date = 0
    for entry in data:
        postedDate = int(entry['postedDate'])
        if postedDate > most_recent_date:
            most_recent_date = postedDate
    return str(most_recent_date)

def filter_data_by_date(data, most_recent_date):
    start_date = str(int(most_recent_date[0:4]) - 1) + most_recent_date[4:6]
    if start_date > most_recent_date:
        start_date = str(int(most_recent_date[0:4]) - 1) + most_recent_date[4:6] 
    filtered_data = [entry for entry in data if start_date <= entry['postedDate'] <= most_recent_date]
    return filtered_data

def calculate_spending_for_category(filtered_data, category):
    spending = sum(float(entry['transactionAmount']) for entry in filtered_data if entry['mechBackItemCode'] == category)
    return spending

with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as f:
    data = json.load(f)
    most_recent_date = find_most_recent_date(data)
    filtered_data = filter_data_by_date(data, most_recent_date)
    spending_for_GROCERY = calculate_spending_for_category(filtered_data, "GROCERY")
    print(f"Spending for GROCERY in the most recent 3 months: {spending_for_GROCERY}")