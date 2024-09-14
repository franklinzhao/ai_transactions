# filename: transaction_data.py
import json
from datetime import datetime

def parse_json_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("File not found")
        return []

def calculate_spending(data):
    # Parse the data and convert the transactionAmount and postedDate to float and datetime respectively
    data = [{'transactionAmount': float(item['transactionAmount']), 'mechBackItemCode': item['mechBackItemCode'], 'postedDate': datetime.strptime(item['postedDate'], '%Y%m%d')} for item in data if item['mechBackItemCode'] == 'GROCERY']

    # Sort the data by postedDate in descending order
    data.sort(key=lambda x: x['postedDate'], reverse=True)

    # Calculate the spending for the newest 3 months
    total_spending = 0
    months = set()
    for item in data:
        month = item['postedDate'].strftime('%Y%m')
        if month in months:
            continue
        months.add(month)
        total_spending += item['transactionAmount']
        if len(months) == 3:
            break

    return total_spending

def main():
    file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
    data = parse_json_data(file_path)
    spending = calculate_spending(data)
    print(f'The total spending for mechBackItemCode equal GROCERY for the newest 3 months is: {spending}')

if __name__ == "__main__":
    main()