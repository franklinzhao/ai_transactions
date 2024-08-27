import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Step 1: Load CSV Data
def load_csv_data(file_path):
    """
    Load data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """
    df = pd.read_csv(file_path)
    return df

# Step 2: Create Embeddings for CSV Data
def create_embeddings(df, column_name, embedding_model='sentence-transformers/all-MiniLM-L6-v2'):
    """
    Create embeddings for the specified column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        column_name (str): The name of the column to create embeddings for.
        embedding_model (str): The HuggingFace model to use for creating embeddings.

    Returns:
        FAISS: A FAISS index with the embeddings.
    """
    # Initialize the embedding model
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

    # Create embeddings for the specified column
    texts = df[column_name].tolist()
    vectors = embeddings.embed_documents(texts)

    # Use FAISS to create a vector store
    faiss_index = FAISS.from_documents(texts, vectors)

    return faiss_index

# Step 3: Implement a Search Mechanism
def search_csv(faiss_index, query, top_k=5):
    """
    Search the FAISS index using a query.

    Args:
        faiss_index (FAISS): The FAISS index with the embeddings.
        query (str): The search query.
        top_k (int): The number of top results to return.

    Returns:
        list: A list of search results.
    """
    # Convert the query to an embedding
    query_vector = faiss_index.embed_query(query)

    # Perform the search
    results = faiss_index.search(query_vector, top_k=top_k)

    return results

# Step 4: Combine Everything into a Search Tool
def csv_search_tool(file_path, query, column_name='content', top_k=5):
    """
    Search a CSV file using a natural language query.

    Args:
        file_path (str): The path to the CSV file.
        query (str): The search query.
        column_name (str): The column name in the CSV to search.
        top_k (int): The number of top results to return.

    Returns:
        list: A list of search results.
    """
    # Load the CSV data
    df = load_csv_data(file_path)

    # Create embeddings
    faiss_index = create_embeddings(df, column_name)

    # Search the data
    results = search_csv(faiss_index, query, top_k)

    return results

# Example Usage
if __name__ == "__main__":
    file_path = "data/customers-100.csv"  # Replace with your actual CSV file path
    query = "Find all records related to AI research"
    results = csv_search_tool(file_path, query, column_name='Company', top_k=5)
    print(results)
