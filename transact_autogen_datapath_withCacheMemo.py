""" 
Project Description:
This transactions ai assist will help summarize transaction amounts by categories.
source my_env/bin/activate
"""

import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process
import random
import os
from customtools import (
    summary_tool_datapath,
    plot_transaction_amount,
    plot_total_transactionAmount_grouped_by_category,
)
from dotenv import load_dotenv
import llms
import json
from data.prepare_data import data_prepared
from mem0 import MemoryClient
import autogen
from data.dataschema import data_description
from autogen.agentchat.contrib.capabilities.teachability import Teachability

load_dotenv()

# datapath = 'data/data_generated100k.json'
datapath = "/home/sagemaker-user/ai_transactions/data/data_generated100k.json"

llm_config = {
    "config_list": [
        {
            "model": "llama-3.1-70b-versatile",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": os.environ["GROQ_API_KEY"],
        },
    ],
    "cache_seed": None,
}

# Let's first define the assistant agent that suggests tool calls.
transactions_insights_assistant = autogen.AssistantAgent(
    name="Transactions Insights Assistant",
    system_message=f"""
    You are a helpful AI assistant.
    Solve tasks using your coding and language skills.
    In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
        1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
        2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
    Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
    When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
    If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
    Reply "TERMINATE" in the end when everything is done.
    
    """,
    llm_config=llm_config,
)

# Instantiate the Teachability capability. Its parameters are all optional. This is actually is Vector DB with Chroma
teachability = Teachability(
        verbosity=1,  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
        reset_db=False,
        path_to_db_dir="./.memory/teachability_db",
        recall_threshold=0.0,  # Higher numbers allow more (but less relevant) memos to be recalled. from 0.0 to 2.0, default 1.5
)

# Now add the Teachability capability(memory via vector DB) to the transactions_insights_assistant.
# teachability.add_to_agent(transactions_insights_assistant)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_task_proxy = autogen.UserProxyAgent(
    name="User Task Proxy",
    system_message="""You are a helpful assistant.  You help complete task and check the final result. """,
    is_termination_msg=lambda msg: msg.get("content") is not None
    and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "ai_generated_code", "use_docker": False},
)
# Register the tool signature with the assistant agent and user proxy agent
autogen.register_function(
    plot_transaction_amount,
    caller=transactions_insights_assistant,
    executor=user_task_proxy,
    name="plot_transaction_amount",
    description=f"""Plot a chart based on transactionAmount and posteddate. 
    The input data file path point to where the data file located.
    The output is plotted chart based on transactionAmount and posteddate.""",
)

autogen.register_function(
    plot_total_transactionAmount_grouped_by_category,
    caller=transactions_insights_assistant,
    executor=user_task_proxy,
    name="plot_total_transactionAmount_grouped_by_category",
    description=f"""
    Plot a bar chart that shows the total transaction amount grouped by category. 
    Each category's total transaction value is displayed on the horizontal axis, 
    helping visualize which categories had positive or negative balances.
    """,
)

dataSchema=dedent(f"""JSON Schema:
                    transactionAmount:
                    Type: string
                    Description: Represents the monetary value of the transaction. It may include both positive (inflow) and negative (outflow) values.
                    mechBackItemCode:
                    Type: string
                    Description: Describes the category or type of the transaction, such as "BANK FEE", "MORTGAGE PAYMENT", "CREDIT CARD PAYMENT", etc.
                    postedDate:
                    Type: string
                    Format: YYYYMMDD
                    Description: Represents the date when the transaction was posted, stored as a string in the format YYYYMMDD. 
""")

finalwords = """Your Final answer must be the response message of plotting result."""
task_description1 = f"""please plot a chart based on transactionAmount and posteddate."""
task_description2 = f"""please plot a bar chart that shows the total transaction amount grouped by category."""
task_description3 = f"""what's the biggest total transactionAmount by mechBackItemCode for 3 month period ended at the last postedDate. 
                        The answer must contain start date and end date of the period along with the total transaction amount."""
task_description4 = dedent(f"""how much spending for GROCERY for 3 month period ended at the last postedDate. 
                        The answer must contain start date and end date of the period along with the total transaction amount.""")
task_description5 = dedent(f"""how much spending for E-TRANSFER in 2022 March?
                        The answer must contain start date and end date of the period along with the total transaction amount.""")
task_prompt = dedent(
                    f"""You will be give this tasks with data, please use your best knowledge to get the right answer:
                        Instructions
                        ------------
                        {task_description5} This is the location of the json data file: {datapath} 
                        This is the schema and meta data of the json data file: {data_description}
  			        """
)

with autogen.Cache.disk(cache_seed=44) as cache:
    user_task_proxy.initiate_chat(transactions_insights_assistant, message=task_prompt, max_turns=None,cache=cache,)

# print(f"""================================\n
# This is the model statistics:\n
#  {final_output.model_dump_json}
#   """)
