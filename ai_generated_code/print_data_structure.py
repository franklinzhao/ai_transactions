# filename: print_data_structure.py

import json

def print_data_structure(data_path):
    # Load the JSON data
    with open(data_path, 'r') as f:
        data = json.load(f)

    # Print the data structure
    print(json.dumps(data, indent=4))

# Call the function
print_data_structure('/home/sagemaker-user/ai_transactions/data/data_generated100k.json')