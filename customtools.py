import math
from crewai_tools import tool
import requests
from bs4 import BeautifulSoup
from crewai_tools import SerperDevTool, CSVSearchTool, JSONSearchTool,TXTSearchTool,PDFSearchTool
import llms
from dotenv import load_dotenv
load_dotenv()

internet_search_tool = SerperDevTool() #"A tool that can be used to search the internet with a search_query."


@tool("Decimal Remove Sum")
def decimalremove_sum_tool(a:float,b:float) -> int:
    """Used for remove decimal from the inputs and then add them together, result is a sum of the integer part of the two numbers ."""
    # Tool logic here
    return math.trunc(a)+math.trunc(b)

@tool("search internet")
def duckduckgo_search(query:str):
    """
    Useful to perform internet search via DuckDuckGo search and return the top results.
    """
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    num_results=3

    if response.status_code != 200:
        raise Exception(f"Error: Unable to fetch search results (status code: {response.status_code})")

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for result in soup.find_all('a', class_='result__a', limit=num_results):
        title = result.text
        link = result['href']
        description_tag = result.find_parent('div', class_='result__body').find('a', class_='result__snippet')
        description = description_tag.text if description_tag else "No description available"
        results.append({'title': title, 'link': link, 'description': description})

    return results


# csv_search_tool = CSVSearchTool(
#     csv='data/csvfile.csv',
#     config=dict(
#         llm=llms.groq_hosted_llm,
#         ),
#         embedder=dict(
#             provider="google", # or openai, ollama, ...
#             config=dict(
#                 model="models/embedding-001",
#                 task_type="retrieval_document",
#                 title="Embeddings",
#             ),
#         ),
#     )

# print(internet_search_tool.run(query="what is microsoft market cap?"))