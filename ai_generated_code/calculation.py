# filename: calculation.py
import json

# Load the data
with open("/home/sagemaker-user/ai_transactions/data/data_generated100k.json", "r") as f:
    data = json.load(f)

# Initialize variables
start_date = "20210301"
end_date = "20210331"
total_amount = 0

# Iterate over the data
for transaction in data:
    if transaction["mechBackItemCode"] == "MORTGAGE PAYMENT" and start_date <= transaction["postedDate"] <= end_date:
        total_amount += float(transaction["transactionAmount"])

print(f"Total spending for MORTGAGE PAYMENT in 2021 March: {total_amount}")
print(f"Date range: {start_date} - {end_date}")