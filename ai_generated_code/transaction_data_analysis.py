# filename: transaction_data_analysis.py
import json

def calculate_spending_for_category(json_data, category, start_date, end_date):
    total_spending = 0
    for transaction in json_data:
        if transaction['mechBackItemCode'] == category and start_date <= transaction['postedDate'] <= end_date:
            total_spending += float(transaction['transactionAmount'])
    return total_spending

def load_json_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Load json data
data = load_json_data('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')

# Define category and dates
category = 'RESTAURANT'
start_date = '20220301'
end_date = '20220331'

# Calculate spending
spending = calculate_spending_for_category(data, category, start_date, end_date)

print(f'Spending for {category} from {start_date} to {end_date}: {spending}')