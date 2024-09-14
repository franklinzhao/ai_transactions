# filename: find_biggest_total_transactionAmount.py
import pandas as pd
import json
from datetime import datetime

# Load the data from the json file
def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Convert data into pandas DataFrame
def convert_to_dataframe(data):
    df = pd.DataFrame(data)
    df['transactionAmount'] = df['transactionAmount'].astype(float)
    df['postedDate'] = pd.to_datetime(df['postedDate'], format='%Y%m%d')
    return df

# Calculate total transactionAmount by mechBackItemCode for the latest 3 months
def calculate_total_transaction_amount(df):
    # Get the latest date
    latest_date = df['postedDate'].max()
    
    # Calculate the date 3 months ago
    three_months_ago = latest_date - pd.DateOffset(months=3)
    
    # Filter the data for the last 3 months
    last_three_months_data = df[(df['postedDate'] > three_months_ago) & (df['postedDate'] <= latest_date)]
    
    # Calculate the total transactionAmount by mechBackItemCode
    total_transaction_amount = last_three_months_data.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index()
    
    return total_transaction_amount

# Find the biggest total transactionAmount
def find_biggest_total_transaction_amount(total_transaction_amount):
    max_amount = total_transaction_amount['transactionAmount'].max()
    max_amount_row = total_transaction_amount[total_transaction_amount['transactionAmount'] == max_amount]
    return max_amount_row

# Main function
def main():
    file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
    data = load_data(file_path)
    df = convert_to_dataframe(data)
    total_transaction_amount = calculate_total_transaction_amount(df)
    max_amount_row = find_biggest_total_transaction_amount(total_transaction_amount)
    print(max_amount_row)

if __name__ == "__main__":
    main()