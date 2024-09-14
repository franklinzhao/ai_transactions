# with open('backItemCodeToTransactionTypeMap.json', 'r') as file:
#     file_contents = file.read()

# # Now the content of the file is stored in the variable 'file_contents'
# task_description=file_contents
# print(task_description)

# Load the task and data from file
import json
with open('data.json', 'r') as file:
    raw_data = json.loads(file.read())

#Preprocess data by only keep fields required
data = []
for item in raw_data:
    extracted_item = {
        'description': item.get('description'),
        'transactionAmount': item.get('transactionAmount'),
        'mechBackItemCode': item.get('mechBackItemCode'),
        'postedDate': item.get('postedDate')
    }
    data.append(extracted_item)

print(json.dumps(data, indent=4))