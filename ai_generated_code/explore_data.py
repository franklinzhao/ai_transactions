# filename: explore_data.py
import json

# Load the json data
try:
    with open('/home/sagemaker-user/ai_transactions/data/data_generated100k.json', 'r') as f:
        data = json.load(f)
except Exception as e:
    print("Failed to load json file:", e)
else:
    # Print the data
    print(json.dumps(data, indent=4))