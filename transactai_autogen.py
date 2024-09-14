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
from customtools import data_summary_tool, decimalremove_sum_tool, duckduckgo_search, internet_search_tool, add_tool,minus_tool,multiple_tool,division_tool, mathpower_tool,squareroot_tool
from dotenv import load_dotenv
import llms 
import json
from data.prepare_data import data_prepared
from mem0 import MemoryClient
import autogen
load_dotenv()

#select preferred large language model
# llm = llms.nvidia_hosted_llm  
# llm = llms.groq_hosted_llm?

#Add memory client to agent
# memory = MemoryClient(api_key=os.environ.get("MEMOAI_APIKEY"))
# conversation = [
#     {
#         "role": "assistant",
#         "content": "Hi, I'm Best Buy's chatbot!\n\nThanks for being a My Best Buy TotalTM member.\n\nWhat can I help you with?",
#     },
#     {
#         "role": "user",
#         "content": 'Seeing horizontal lines on our tv. TV model: Sony - 77" Class BRAVIA XR A80K OLED 4K UHD Smart Google TV',
#     },
#     {
#         "role": "assistant",
#         "content": "Thanks for being a My Best Buy Total™ member. I can connect you to an expert immediately - just one perk of your membership!\n\nSelect the button below when you're ready to chat.",
#     },
#     {
#         "role": "assistant",
#         "content": "Good evening, thank you for choosing Best Buy, Fnu. My name is Lovely. I hope you are doing well. I'm sorry to hear that you're seeing horizontal lines on your TV.\n\nI'm absolutely committed to exploring all possible ways to assist you to fix this issue.\n\nTo ensure that we are on the right account, may I please have your email address registered with your Best Buy account?",
#     },
#     {"role": "user", "content": "dd@gmail.com"},
#     {
#         "role": "assistant",
#         "content": "Perfect! Thank you for providing all the details, surely you have made my job easier by doing this. I really appreciate it.\n\nI also want to take a moment to express our heartfelt appreciation for your trust and loyalty. Thank you for being an amazing customer of BestBuy Total.\n\nCould you please help me with the order number or product's details to check it quickly?\n\nSamsung - 49\" Odyssey OLED G9 (G95SC) DQHD 240Hz 0.03ms G-Sync Compatible Curved Smart Gaming Monitor - Silver - just to confirm this is the item, right?",
#     },
#     {"role": "user", "content": "Order number: 112217629"},
#     {
#         "role": "assistant",
#         "content": "Superb! Thank you for confirmation.\n\nThank you for your patience. After exploring all possible solutions, I can help you to arrange a home repair appointment for your device. Our Geek Squad experts will visit your home to inspect and fix your device.\n\nIt's great that you have a protection plan - rest assured, we've got your back! As a valued Total member, you can avail this service at a minimal service fee. This fee, applicable to all repairs, covers the cost of diagnosing the issue and any small parts needed for the repair. It's part of our 24-month free protection plan.\n\nPlease click here to review the service fee and plan coverage details -\n\nhttps://www.bestbuy.com/site/best-buy-membership/best-buy-protection/pcmcat1608643232014.c?id=pcmcat1608643232014#jl-servicefees\n\nFnu - just to confirm shall I proceed to schedule the appointment?",
#     },
#     {"role": "user", "content": "Yes please"},
#     {"role": "assistant", "content": "When should I schedule the appointment?"},
#     {"role": "user", "content": "Schedule it for tomorrow please"},
# ]

# memory.add(messages=conversation, user_id="customer_service_bot")
# data2 = "I forgot the order numnber, can you quickly tell me?"

# relevant_memories = memory.search(data2, user_id="customer_service_bot")
# flatten_relevant_memories = "\n".join([m["memory"] for m in relevant_memories])
# print(flatten_relevant_memories)

#Use preprocessed data by only keep fields required
# data = data_prepared('data/data.json')

#Use generated data
with open('data/data_generated.json', 'r') as file:
    # read files as string and convert to json object
    data = json.loads(file.read()) 

# Get user inputs
# task_description = input("How can I help you today?\n")


llm_config = {
    "config_list": [
        {
            "model": "llama-3.1-70b-versatile",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": "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",
        },
    ],
    "cache_seed": None,
}
# Let's first define the assistant agent that suggests tool calls.
transactions_assist = autogen.ConversableAgent(
    name="Transaction Insights Assistant",
    system_message="You are a helpful AI assistant. "
                   "Return 'TERMINATE' when the task is done.",
    llm_config=llm_config
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_task_proxy = autogen.ConversableAgent(
    name="User Task Proxy",
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the tool signature with the assistant agent.
transactions_assist.register_for_llm(name="data_summary_tool", description=f"""Summarizes the transaction data. The input data is a JSON list in string format.
    The output is a summary report in JSON format, sorted by transactionAmount in descending order.""")(data_summary_tool)


# Register the tool function with the user proxy agent.
user_task_proxy.register_for_execution(name="data_summary_tool")(data_summary_tool)

task_description=f"""I have this json data, please summarize total of transactionamount with mechbackitemcode 
                    and find the top 3 by total transactionamount."""
task_prompt = dedent(f"""You will be give this tasks with data, please use your best knowledge to get the right answer:
                
                            Instructions
                            ------------
                        {task_description} This is the json data: {data}                
                            Your Final answer must use this template format:
                            
                            Top 3 by total transaction amount:
                            MORTGAGE: $301.01
                            ENTERTAINMENT: $98.89
                            RESTAURANT: $45.23

  			        """)

user_task_proxy.initiate_chat(
    transactions_assist,
    message=task_prompt
)

# print(f"""================================\n
# This is the model statistics:\n 
#  {final_output.model_dump_json} 
#   """)