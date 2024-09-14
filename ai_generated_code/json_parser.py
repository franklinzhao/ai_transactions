# filename: json_parser.py
import json
from datetime import datetime

# Load the JSON data from the file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Print the dates of the transactions
def print_transaction_dates(data):
    for transaction in data:
        print(transaction['postedDate'])

# Main function
def main():
    file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
    data = load_json_data(file_path)
    print("Transaction dates:")
    print_transaction_dates(data)

if __name__ == '__main__':
    main()