import requests
from langchain.tools import BaseTool
from langchain import LLMChain, OpenAI
from langchain.prompts import PromptTemplate

# Step 1: Define the Backend API Tool
class BackendAPITool(BaseTool):
    name = "Backend API Caller"
    description = "A tool that sends a JSON request to a backend API and returns the response."

    def __init__(self, api_url: str):
        self.api_url = api_url

    def _run(self, query: str):
        # Prepare the JSON payload
        payload = {"query": query}

        # Send the JSON request to the backend API
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Raise an error for bad HTTP status codes
            return response.json()  # Return the JSON response directly
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as req_err:
            return f"Request error occurred: {req_err}"
        except Exception as err:
            return f"An unexpected error occurred: {err}"

    def _arun(self, query: str):
        raise NotImplementedError("Async version not implemented")

# Step 2: Integrate the tool in a LangChain pipeline
def create_backend_api_chain(api_url: str, query: str):
    # Initialize the BackendAPITool with the provided API URL
    tool = BackendAPITool(api_url=api_url)

    # Run the tool to get the API response
    api_results = tool.run(query)

    # Create a prompt template to structure the interaction between the tool and the LLM
    template = """Given the following query and API results, generate a response:
    Query: {query}
    API Results: {api_results}"""

    prompt = PromptTemplate(template=template, input_variables=["query", "api_results"])

    # Create an LLMChain with the OpenAI model and the prompt template
    llm = OpenAI(temperature=0.5)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Use the chain to process the query and API results
    output = chain.run({"query": query, "api_results": api_results})

    return output

# Example usage
if __name__ == "__main__":
    api_url = "https://example.com/api/endpoint"  # Replace with your actual API URL
    query = "Fetch the latest data on AI research"
    output = create_backend_api_chain(api_url, query)
    print(output)
