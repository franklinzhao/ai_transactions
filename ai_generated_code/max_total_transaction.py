# filename: max_total_transaction.py

import json
import pandas as pd

def max_total_transaction():
    data_file = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
    
    # Read the JSON data file
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    
    # Convert 'transactionAmount' to float
    df['transactionAmount'] = df['transactionAmount'].astype(float)
    
    # Group by 'mechBackItemCode' and sum 'transactionAmount'
    df_grouped = df.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index()
    
    # Find the maximum total transaction amount
    max_amount = df_grouped['transactionAmount'].max()
    max_amount_code = df_grouped.loc[df_grouped['transactionAmount'].idxmax()]['mechBackItemCode']
    
    print('The maximum total transaction amount by mechBackItemCode for all time is: ')
    print(f'{max_amount_code}: {max_amount}')

max_total_transaction()