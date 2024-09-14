import json
import random
from datetime import datetime, timedelta
from random import randint, uniform

def generate_data(number:int):
    # Create an empty list to store the JSON objects
    json_list = []

    # Define some sample data for randomization
    descriptions = ["HOTEL MONTREAL", "RESTAURANT QUEBEC", "GROCERY STORE WONDERFUL", "GAS STATION PETRO CANADA"]
    mechBackItem_codes = [
        "MORTGAGE PAYMENT", 
        "CREDIT CARD PAYMENT", 
        "LOAN PAYBACK", 
        "RESTAURANT",
        "BANK FEE",
        "TAX PAYMENT",
        "INTEREST DEPOSIT",
        "GROCERY",
        "GASOLINE",
        "E-TRANSFER",
        "FOREIGNEXCHANGE PAYMENT",
        "CHEQUE DEPOSIT",
        "WAGE",
        "WIRE IN",
        "WIRE OUT"
        ]
    debitCreditIndicators =["","-"]

    # Generate JSON objects with randomized fields
    for i in range(number):
        # Create a new dictionary based on the base JSON object
        new_json = {} 
        
        # Randomize the description
        # new_json["description"] = random.choice(descriptions)
        
        # Randomize the transaction amount
        new_json["transactionAmount"] = random.choice(debitCreditIndicators)+str(round(uniform(10.0, 1000.0), 2))
        
        # Randomize the mech back item code
        new_json["mechBackItemCode"] = random.choice(mechBackItem_codes)
        
        # Modify the posted date by adding random days
        random_date = datetime(2021, 1, 1) + timedelta(days=random.randint(0, 730)) #two years data
        # Convert the dates to the desired format
        new_json["postedDate"] = random_date.strftime("%Y%m%d")

        # Append the new JSON object to the list
        json_list.append(new_json)
    return json_list

# Print the JSON string
# json_string = json.dumps(json_list, indent=4)
# print(json_string)

def save_tolocal(filename:str, number:int):
    # Open a file for writing
    with open(filename, "w") as file:
        # Write the list of JSON objects to the file
        json_list=generate_data(number)
        json.dump(json_list, file, indent=4)

save_tolocal("data_generated100k.json",100000)