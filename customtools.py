import math
from crewai_tools import tool
import requests
from bs4 import BeautifulSoup
from crewai_tools import SerperDevTool, CSVSearchTool, JSONSearchTool,TXTSearchTool,PDFSearchTool
import llms
import json
import pandas as pd
from typing import Annotated, Dict
from typing_extensions import TypedDict, List
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

load_dotenv()

internet_search_tool = SerperDevTool() #"A tool that can be used to search the internet with a search_query."


@tool("Decimal Remove Sum")
def decimalremove_sum_tool(a:float,b:float) -> int:
    """Used for remove decimal from the inputs and then add them together, result is a sum of the integer part of the two numbers ."""
    # Tool logic here
    return math.trunc(a)+math.trunc(b)

@tool("add")
def add_tool(a:float,b:float) -> float:
    """Used for add two nubmers together, result is a sum of the two numbers ."""
    return a+b

@tool("minus")
def minus_tool(a:float,b:float) -> float:
    """Used for minus two nubmers, result is minus of the two numbers ."""
    return a-b

@tool("multiple")
def multiple_tool(a:float,b:float) -> float:
    """Used for multiple two nubmers, result is a multiple of the two numbers ."""
    return a*b

@tool("division")
def division_tool(a:float,b:float) -> float:
    """Used for divide one number to the other, result is a division of the two numbers ."""
    if b != 0:
        return a/b
    else:
        raise Exception("Error: divide 0 is not allowed!")


@tool("math power tool")
def mathpower_tool(a:float,b:float) -> float:
    """Used for a to the power of b."""
    return math.pow(a,b)

@tool("square root")
def squareroot_tool(a:float) -> float:
    """Used for multiple the two numbers and then get square root of it."""
    return math.sqrt(a)

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

@tool("Summarize transactions data")
def data_summary_tool_crewai(data: Annotated[str,"a string representing JSON data"])->json:
    """
    Summarizes the transaction data. The input data is a JSON list in string format.
    The output is a summary report in JSON format which been sorted by transactionAmount in descending order.
    """
     # Convert JSON data to Python object
    json_data = str.replace(data,"'",'"')
    data = json.loads(json_data)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Convert 'transactionAmount' to float
    df['transactionAmount'] = df['transactionAmount'].astype(float)

    # Group by 'mechBackItemCode' and sum 'transactionAmount'
    summary = df.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index().sort_values(by='transactionAmount', ascending=False)
    return summary.to_json(orient='records')


def data_summary_tool(data: Annotated[str, "A JSON Formatted String enclosed in triple-quotation"])->json:
    """
    Summarizes the transaction data. The input data is a JSON list in string format.
    The output is a summary report in JSON format which been sorted by transactionAmount in descending order.
    """
     # Convert JSON data to Python object
    json_data = str.replace(data,"'",'"')
    data = json.loads(json_data)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Convert 'transactionAmount' to float
    df['transactionAmount'] = df['transactionAmount'].astype(float)

    # Group by 'mechBackItemCode' and sum 'transactionAmount'
    summary = df.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index().sort_values(by='transactionAmount', ascending=False)
    return summary.to_json(orient='records')

def summary_tool_datapath(datapath: Annotated[str, "data file path in string"])->json:
    """
    Summarizes the transaction data. The input data file path point to where the data file located.
    The output is a summary report in JSON format which been sorted by transactionAmount in descending order.
    """
    #load data from datapath
    with open(datapath, 'r') as file:
        data = json.loads(file.read()) 
    # print(data)
     # Convert JSON data to Python object
    # json_data = str.replace(data,"'",'"')
    # data = json.loads(data)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Convert 'transactionAmount' to float
    df['transactionAmount'] = df['transactionAmount'].astype(float)

    # Group by 'mechBackItemCode' and sum 'transactionAmount'
    summary = df.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index().sort_values(by='transactionAmount', ascending=False)
    return summary.to_json(orient='records')

@tool("Summarize transactions data")
def summary_tool_datapath_crewai(datapath: Annotated[str, "data file path in string"])->json:
    """
    Summarizes the transaction data. The input data file path point to where the data file located.
    The output is a summary report in JSON format which been sorted by transactionAmount in descending order.
    """
    #load data from datapath
    with open(datapath, 'r') as file:
        data = json.loads(file.read()) 
    # print(data)
     # Convert JSON data to Python object
    # json_data = str.replace(data,"'",'"')
    # data = json.loads(data)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Convert 'transactionAmount' to float
    df['transactionAmount'] = df['transactionAmount'].astype(float)

    # Group by 'mechBackItemCode' and sum 'transactionAmount'
    summary = df.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index().sort_values(by='transactionAmount', ascending=False)
    return summary.to_json(orient='records')
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
# data="""[{'transactionAmount': '100.560001', 'mechBackItemCode': 'MORTGAGE', 'postedDate': '20230125'}, {'transactionAmount': '100.44', 'mechBackItemCode': 'MORTGAGE', 'postedDate': '20230125'}, {'transactionAmount': '100.01', 'mechBackItemCode': 'MORTGAGE', 'postedDate': '20230125'}, {'transactionAmount': '98.89', 'mechBackItemCode': 'ENTERTAINMENT', 'postedDate': '20231025'}, {'transactionAmount': '45.23', 'mechBackItemCode': 'RESTAURANT', 'postedDate': '20230925'}, {'transactionAmount': '68.78', 'mechBackItemCode': 'GROCERY', 'postedDate': '20230625'}, {'transactionAmount': '-208.22', 'mechBackItemCode': 'GROCERY', 'postedDate': '20240625'}]"""
# print(data_summary_tool(data))

# print(summary_tool_datapath("data/data_generated100k.json"))

def plot_transaction_amount(datapath: Annotated[str, "data file path in string"])->str:
    """
    Plot a chart based on transactionAmount and posteddate. 
    The input data file path point to where the data file located.
    The output is plotted chart based on transactionAmount and posteddate.
    """
    with open(datapath, 'r') as file:
        data = json.loads(file.read())

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Convert transactionAmount to float
    df['transactionAmount'] = df['transactionAmount'].astype(float)

    # Convert postedDate to datetime
    df['postedDate'] = pd.to_datetime(df['postedDate'], format='%Y%m%d')

    # Sort by postedDate
    df = df.sort_values(by='postedDate')

    # Calculate cumulative sum
    df['cumulative_sum'] = df['transactionAmount'].cumsum()

    # Plot cumulative sum by postedDate
    plt.figure(figsize=(10, 6))
    plt.plot(df['postedDate'], df['cumulative_sum'], marker='o')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    plt.title('Cumulative Sum of Transaction Amount by Posted Date')
    plt.xlabel('Posted Date')
    plt.ylabel('Cumulative Sum of Transaction Amount')
    plt.grid(True)
    plt.savefig('chart/plotChart_CumulativeSumofTransactionAmount.png')
    return f""" chart is plotted and saved in chart folder as: plotChart_CumulativeSumofTransactionAmount.png """

def plot_total_transactionAmount_grouped_by_category(datapath: Annotated[str, "data file path in string"])->str:
    """
    Plot a bar chart that shows the total transaction amount grouped by category. 
    Each category's total transaction value is displayed on the horizontal axis, 
    helping visualize which categories had positive or negative balances.
    """
    with open(datapath, 'r') as file:
        data = json.loads(file.read())

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Convert 'transactionAmount' to float and 'postedDate' to datetime
    df['transactionAmount'] = df['transactionAmount'].astype(float)
    df['postedDate'] = pd.to_datetime(df['postedDate'], format='%Y%m%d')

    # Aggregate transaction amounts by 'mechBackItemCode' (category)
    grouped_data = df.groupby('mechBackItemCode')['transactionAmount'].sum().reset_index()

    # Plot
    plt.figure(figsize=(10, 6))
    plt.barh(grouped_data['mechBackItemCode'], grouped_data['transactionAmount'], color='skyblue')
    plt.xlabel('Total Transaction Amount')
    plt.ylabel('Transaction Category')
    plt.title('Total Transaction Amount by Category')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig('chart/plotChart_total_transactionAmount_grouped_by_category.png')
    return f""" chart is plotted and saved in chart folder as: plotChart_total_transactionAmount_grouped_by_category.png """
          

#Testing...........
# plot_transaction_amount('data/data_generated100k.json')
# plot_total_transactionAmount_grouped_by_category('data/data_generated100k.json')