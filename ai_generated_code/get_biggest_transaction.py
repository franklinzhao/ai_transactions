# filename: get_biggest_transaction.py
import json

def get_biggest_transaction(datapath):
    with open(datapath, 'r') as f:
        data = json.load(f)

    # Filter data to only include items with the correct keys
    valid_items = [item for item in data 
                    if 'postedDate' in item 
                    and 'mechBackItemCode' in item 
                    and 'transactionAmount' in item]

    # Find the biggest transactionAmount by mechBackItemCode
    biggest_transactions = {}
    for item in valid_items:
        mechbackitemcode = item['mechBackItemCode']
        if mechbackitemcode not in biggest_transactions or float(item['transactionAmount']) > float(biggest_transactions[mechbackitemcode]['transactionAmount']):
            biggest_transactions[mechbackitemcode] = item

    # Print the top N mechBackItemCodes with the biggest transaction amounts
    top_n = 10
    sorted_biggest_transactions = sorted(biggest_transactions.items(), key=lambda x: float(x[1]['transactionAmount']), reverse=True)
    print("Top {} mechBackItemCodes with the biggest transaction amounts:".format(top_n))
    for i in range(min(top_n, len(sorted_biggest_transactions))):
        mechbackitemcode, item = sorted_biggest_transactions[i]
        print("{}: {}".format(mechbackitemcode, item['transactionAmount']))

get_biggest_transaction('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')