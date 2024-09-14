# filename: find_spending.py
import json

# define the location of the data file
data_path = '/home/sagemaker-user/ai_transactions/data/data_generated100k.json'

# define the date range for March 2022
start_date = '20220301'
end_date = '20220331'

# define the category
category = 'RESTAURANT'

# initialize total spending
total_spending = 0

# open the data file
with open(data_path, 'r') as file:
    # load the json data
    data = json.load(file)

    # loop over each transaction
    for transaction in data:
        # check if the transaction date is within the specified range and the category is 'RESTAURANT'
        if start_date <= transaction['postedDate'] <= end_date and transaction['mechBackItemCode'] == category:
            # add the transaction amount to the total spending
            total_spending += float(transaction['transactionAmount'])

# print the total spending for 'RESTAURANT' in '2022 March'
print(f'Total spending for {category} in 2022 March: {total_spending}')
print(f'Date range: {start_date} - {end_date}')