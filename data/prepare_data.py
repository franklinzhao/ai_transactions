import json

def data_prepared(file_path:str)->[]:
    """
    Prepare the data get from api, remove un-used fields to reduce data size, save cost.
    """
    # Load the task and data from file
    with open(file_path, 'r') as file:
        raw_data = json.loads(file.read()) #read files as string and convert to json object

    #Preprocess data by only keep fields required
    data = []
    for item in raw_data:
        # Apply the minus sign if debit
        signed_transactionAmount=0
        if item.get('debitCreditIndicator') == '-':
            signed_transactionAmount = '-' + str(item.get('transactionAmount'))
        else:
            signed_transactionAmount = str(item.get('transactionAmount'))
        extracted_item = {
            # 'description': item.get('description'),
            'transactionAmount': signed_transactionAmount,
            'mechBackItemCode': item.get('mechBackItemCode'),
            'postedDate': item.get('postedDate'),
            # 'debitCreditIndicator': item.get('debitCreditIndicator')
        }
        data.append(extracted_item)
    return data

# print(json.dumps(data_prepared('data.json'), indent=4))