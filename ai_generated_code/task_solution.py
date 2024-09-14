# filename: task_solution.py

import json
import pandas as pd

def get_biggest_total_transaction():
    datapath = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'

    with open(datapath) as json_file:
        data = json.load(json_file)

    # Convert the data to a pandas DataFrame for easier manipulation
    df = pd.json_normalize(data)

    # Convert 'postedDate' to datetime
    df['postedDate'] = pd.to_datetime(df['postedDate'], format='%Y%m%d')

    # Convert 'transactionAmount' to numeric
    df['transactionAmount'] = pd.to_numeric(df['transactionAmount'])

    # Get the end date of the period
    end_date = df['postedDate'].max()

    # Calculate the start date of the period
    start_date = end_date - pd.DateOffset(months=3)

    # Filter the data for the 3 month period
    filtered_df = df[(df['postedDate'] <= end_date) & (df['postedDate'] >= start_date)]

    # Group the data by mechBackItemCode and sum the transactionAmount
    total_transaction_amount = filtered_df.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index()

    # Get the mechBackItemCode with the biggest total transaction amount
    biggest_total_amount_item = total_transaction_amount.loc[total_transaction_amount['transactionAmount'].idxmax()]

    # Convert the start date and end date back to string in the format 'YYYYMMDD'
    start_date_str = start_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')

    print(f"Start date of the period: {start_date_str}")
    print(f"End date of the period: {end_date_str}")
    print(f"mechBackItemCode with the biggest total transaction amount: {biggest_total_amount_item['mechBackItemCode']}")
    print(f"Biggest total transaction amount: {biggest_total_amount_item['transactionAmount']}")

get_biggest_total_transaction()