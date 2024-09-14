# filename: transaction_analyzer.py
import json
import pandas as pd
from datetime import datetime

def get_biggest_total_transaction_amount(json_data_path):
    with open(json_data_path, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # Convert postedDate to datetime
    df['postedDate'] = pd.to_datetime(df['postedDate'], format='%Y%m%d')
    
    # Convert transactionAmount to float
    df['transactionAmount'] = df['transactionAmount'].astype(float)
    
    # Filter data for the newest 3 months
    three_months_ago = datetime.now() - pd.DateOffset(months=3)
    df = df[df['postedDate'] > three_months_ago]
    
    # Group by mechBackItemCode and calculate total transactionAmount
    total_transaction_amount = df.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index()
    
    # Sort by total transactionAmount in descending order
    total_transaction_amount = total_transaction_amount.sort_values(by='transactionAmount', ascending=False)
    
    # Check if total_transaction_amount is empty
    if not total_transaction_amount.empty:
        # Print the mechBackItemCode with the biggest total transactionAmount
        print(total_transaction_amount.iloc[0]['mechBackItemCode'])
        print(total_transaction_amount.iloc[0]['transactionAmount'])
    else:
        print("No transactions found in the last 3 months.")

get_biggest_total_transaction_amount('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')