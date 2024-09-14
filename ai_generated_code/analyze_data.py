# filename: analyze_data.py
import json
import pandas as pd
from datetime import datetime, timedelta

# Load the data from the JSON file
def load_data(data_path):
    with open(data_path, 'r') as f:
        data = json.load(f)
    return data

# Convert the JSON data to a pandas DataFrame
def json_to_df(data):
    df = pd.DataFrame(data)
    # Convert the transactionAmount to numeric values
    df['transactionAmount'] = pd.to_numeric(df['transactionAmount'])
    # Convert the postedDate to datetime objects
    df['postedDate'] = pd.to_datetime(df['postedDate'], format='%Y%m%d')
    return df

# Filter the data for the last 3 months and mechBackItemCode equal to GROCERY
def filter_data(df):
    # Calculate the date 3 months ago
    three_months_ago = datetime.now() - timedelta(days=90)
    # Filter the data
    filtered_df = df[(df['postedDate'] >= three_months_ago) & (df['mechBackItemCode'] == 'GROCERY')]
    return filtered_df

# Calculate the total spending for the filtered data
def calculate_spending(df):
    total_spending = df['transactionAmount'].sum()
    return total_spending

# Main function
def main():
    data_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
    data = load_data(data_path)
    df = json_to_df(data)
    filtered_df = filter_data(df)
    total_spending = calculate_spending(filtered_df)
    print('Total spending for mechBackItemCode equal GROCERY for most recent 3 month:', total_spending)

if __name__ == '__main__':
    main()