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
from customtools import data_summary_tool_crewai, decimalremove_sum_tool, duckduckgo_search, internet_search_tool, add_tool,minus_tool,multiple_tool,division_tool, mathpower_tool,squareroot_tool
from dotenv import load_dotenv
import llms 
import json
from data.prepare_data import data_prepared
from mem0 import MemoryClient
load_dotenv()

#select preferred large language model
# llm = llms.nvidia_hosted_llm  
llm = llms.groq_hosted_llm

#Add memory client to agent
memory = MemoryClient(api_key=os.environ.get("MEMOAI_APIKEY"))
conversation = [
    {
        "role": "assistant",
        "content": "Hi, I'm Best Buy's chatbot!\n\nThanks for being a My Best Buy TotalTM member.\n\nWhat can I help you with?",
    },
    {
        "role": "user",
        "content": 'Seeing horizontal lines on our tv. TV model: Sony - 77" Class BRAVIA XR A80K OLED 4K UHD Smart Google TV',
    },
    {
        "role": "assistant",
        "content": "Thanks for being a My Best Buy Total™ member. I can connect you to an expert immediately - just one perk of your membership!\n\nSelect the button below when you're ready to chat.",
    },
    {
        "role": "assistant",
        "content": "Good evening, thank you for choosing Best Buy, Fnu. My name is Lovely. I hope you are doing well. I'm sorry to hear that you're seeing horizontal lines on your TV.\n\nI'm absolutely committed to exploring all possible ways to assist you to fix this issue.\n\nTo ensure that we are on the right account, may I please have your email address registered with your Best Buy account?",
    },
    {"role": "user", "content": "dd@gmail.com"},
    {
        "role": "assistant",
        "content": "Perfect! Thank you for providing all the details, surely you have made my job easier by doing this. I really appreciate it.\n\nI also want to take a moment to express our heartfelt appreciation for your trust and loyalty. Thank you for being an amazing customer of BestBuy Total.\n\nCould you please help me with the order number or product's details to check it quickly?\n\nSamsung - 49\" Odyssey OLED G9 (G95SC) DQHD 240Hz 0.03ms G-Sync Compatible Curved Smart Gaming Monitor - Silver - just to confirm this is the item, right?",
    },
    {"role": "user", "content": "Order number: 112217629"},
    {
        "role": "assistant",
        "content": "Superb! Thank you for confirmation.\n\nThank you for your patience. After exploring all possible solutions, I can help you to arrange a home repair appointment for your device. Our Geek Squad experts will visit your home to inspect and fix your device.\n\nIt's great that you have a protection plan - rest assured, we've got your back! As a valued Total member, you can avail this service at a minimal service fee. This fee, applicable to all repairs, covers the cost of diagnosing the issue and any small parts needed for the repair. It's part of our 24-month free protection plan.\n\nPlease click here to review the service fee and plan coverage details -\n\nhttps://www.bestbuy.com/site/best-buy-membership/best-buy-protection/pcmcat1608643232014.c?id=pcmcat1608643232014#jl-servicefees\n\nFnu - just to confirm shall I proceed to schedule the appointment?",
    },
    {"role": "user", "content": "Yes please"},
    {"role": "assistant", "content": "When should I schedule the appointment?"},
    {"role": "user", "content": "Schedule it for tomorrow please"},
]

memory.add(messages=conversation, user_id="customer_service_bot")
data2 = "I forgot the order numnber, can you quickly tell me?"

relevant_memories = memory.search(data2, user_id="customer_service_bot")
flatten_relevant_memories = "\n".join([m["memory"] for m in relevant_memories])
print(flatten_relevant_memories)

#Use preprocessed data by only keep fields required
# data = data_prepared('data/data.json')

#Use generated data     #read files as string and convert to json object
with open('data/data_generated.json', 'r') as file:
    data = json.loads(file.read()) 

# Get user inputs
# task_description = input("How can I help you today?\n")
task_description="""I have this json data, please summarize total of transactionamount with mechbackitemcode 
and find the top 3 by total transactionamount."""

# Define an Agent
"""
    Attributes:
            agent_executor: An instance of the CrewAgentExecutor class.
            role: The role of the agent.
            goal: The objective of the agent.
            backstory: The backstory of the agent.
            config: Dict representation of agent configuration.
            llm: The language model that will run the agent.
            function_calling_llm: The language model that will handle the tool calling for this agent, it overrides the crew function_calling_llm.
            max_iter: Maximum number of iterations for an agent to execute a task.
            memory: Whether the agent should have memory or not.
            max_rpm: Maximum number of requests per minute for the agent execution to be respected.
            verbose: Whether the agent execution should be in verbose mode.
            allow_delegation: Whether the agent is allowed to delegate tasks to other agents.
            tools: Tools at agents disposal
            step_callback: Callback to be executed after each step of the agent execution.
            callbacks: A list of callback functions from the langchain library that are triggered during the agent's execution process
            allow_code_execution: Enable code execution for the agent.
            max_retry_limit: Maximum number of retries for an agent to execute a task when an error occurs.
"""
transactions_assist = Agent(
    llm=llm,
    role='transactions assistant',
    goal='summarize transactionAmount by mechBackItemCode',
    backstory=dedent("""Instructions
                        You are a transactions assistant at a bank. 
                        You expertise is summarize transactionAmount by mechBackItemCode.
                        Do your best to produce the correct summary report. 
                    """),
    allow_delegation=False,
    verbose=True,
    # tools=[decimalremove_sum_tool,internet_search_tool, add_tool,minus_tool,multiple_tool,division_tool, mathpower_tool,squareroot_tool],
    tools=[data_summary_tool_crewai],
    memory=True,
    # function_calling_llm=firework_hosted_llama,
    tools_results=[],
    max_iter=100
)

# Define task
transactions_analysis_task = Task(
    llm=llm,
    description=dedent(f"""You will be give this tasks with data, please use your best knowledge to get the right answer:
                
                            Instructions
                            ------------
                        {task_description} This is the json data: {data}                
                            Your Final answer must use this template format:
                            
                            Top 3 by total transaction amount:
                            MORTGAGE: $301.01
                            ENTERTAINMENT: $98.89
                            RESTAURANT: $45.23

  			        """),
    expected_output="A summary report with total transactionAmount along with mechBackItemCode. Don't use json format.",
    agent=transactions_assist,
    # tools=[data_summary_tool_crewai],
    human_input=False
)

# Define the team
crew = Crew(
  agents=[transactions_assist],
  tasks=[transactions_analysis_task],
  verbose=True      
)

# Start work on the task
final_output = crew.kickoff()

# Print output
print(f"""########################
\nHere is the Final Result:\n
########################\n
{final_output}
\n """)

print(f"""================================\n
This is the model statistics:\n 
 {final_output.model_dump_json} 
  """)