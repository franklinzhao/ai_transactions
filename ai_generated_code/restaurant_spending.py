# filename: restaurant_spending.py
import json

# Define the input parameters
data_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
start_date = '20220301'
end_date = '20220331'
category = 'RESTAURANT'

# Initialize the total spending
total_spending = 0

# Load the JSON data file
with open(data_path, 'r') as file:
    for line in file:
        try:
            data = json.loads(line)
            # Check if the transaction is for the specified category and date range
            if data['mechBackItemCode'] == category and start_date <= data['postedDate'] <= end_date:
                # Add the transaction amount to the total spending
                total_spending += float(data['transactionAmount'])
        except json.JSONDecodeError:
            print(f"Skipping line: {line}")

# Print the result
print(f'Total spending for {category} from {start_date} to {end_date}: ${total_spending:.2f}')