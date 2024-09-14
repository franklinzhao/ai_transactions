# Define the schema
json_schema = {
    "transactionAmount": {
        "type": "string",
        "description": "Represents the monetary value of the transaction. It may include both positive (inflow) and negative (outflow) values."
    },
    "mechBackItemCode": {
        "type": "string",
        "description": "Describes the category or type of the transaction, such as 'BANK FEE', 'MORTGAGE PAYMENT', etc."
    },
    "postedDate": {
        "type": "string",
        "format": "YYYYMMDD",
        "description": "Represents the date when the transaction was posted, stored as a string in the format YYYYMMDD."
    }
}

# Metadata: total transactions, date range, unique mechBackItemCode categories
metadata = {
    "total_transactions": 100000,
    "date_range": {
        "start": "20210101",
        "end": "20230101"
    },
    "unique_categories": [
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
}

# Simulating storing in memory
data_description = {
    "schema": json_schema,
    "metadata": metadata
}

# This memory can now be used in the LLM to answer queries related to the data.

# Summary of Key Techniques:
# Schema and Metadata in Memory: Quick access to schema and key metadata for high-level questions.
# Chunking: Split large data into smaller chunks (e.g., by month or category) for better memory efficiency.
# External Storage: Store large data in a scalable system (e.g., AWS S3, database) and retrieve relevant chunks dynamically based on queries.
# Dynamic Retrieval: Use user input to fetch relevant chunks of data in real-time, keeping memory usage within limits.