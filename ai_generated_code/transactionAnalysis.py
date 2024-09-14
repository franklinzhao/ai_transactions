# filename: transactionAnalysis.py
import json
import pandas as pd

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def find_biggest_transaction_amount(df, category):
    return df[df['mechBackItemCode'] == category]['transactionAmount'].max()

def main():
    file_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'
    df = load_data(file_path)
    category = 'GROCERY'
    biggest_transaction_amount = find_biggest_transaction_amount(df, category)
    print(f"The biggest transaction amount for the '{category}' category is: {biggest_transaction_amount}")

if __name__ == "__main__":
    main()