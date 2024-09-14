# filename: verify_transactions.py
import json

# Load the JSON data file
with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as f:
    data = json.load(f)

# Define the parameters for the period
start_date = '20220301'
end_date = '20220331'

# Initialize a flag to check if there are any transactions
has_transactions = False

# Check if there are any CHEQUE DEPOSIT transactions
for transaction in data:
    if start_date <= transaction['postedDate'] <= end_date and transaction['mechBackItemCode'] == 'CHEQUE DEPOSIT':
        has_transactions = True
        break

# Print the result
if has_transactions:
    print("There are CHEQUE DEPOSIT transactions in the data from 20220301 to 20220331.")
else:
    print("There are no CHEQUE DEPOSIT transactions in the data from 20220301 to 20220331.")