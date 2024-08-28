""" 
Project Description:
This transactions ai assist will help summarize transaction amounts by categories with time.
"""

import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process
import random
import os
from customtools import decimalremove_sum_tool, duckduckgo_search, internet_search_tool, add_tool,minus_tool,multiple_tool,division_tool, mathpower_tool,squareroot_tool
from dotenv import load_dotenv
import llms 
load_dotenv()

llm = llms.groq_hosted_llm  #select preferred large language model

# Load the task and data from file
with open('data/data.txt', 'r') as file:
    data = file.read()


# Get user inputs
# task_description = input("How can I help you today?\n")
task_description="I have this json data, please summarize total of transactionamount with mechbackitemcode."

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
                        You expertise is in summarize transactionAmount by mechBackItemCode.
                        Do your best to produce the correct summary report.
                    """),
    allow_delegation=False,
    verbose=True,
    # tools=[decimalremove_sum_tool,internet_search_tool, add_tool,minus_tool,multiple_tool,division_tool, mathpower_tool,squareroot_tool],
    # tools=[decimalremove_sum_tool(result_as_answer=True)],
    memory=True,
    # function_calling_llm=firework_hosted_llama,
    tools_results=[],
    max_iter=50 
)

# Define task
transactions_analysis_task = Task(
    llm=llm,
    description=dedent(f"""You will be give this tasks with data, please use your best knowledge to get the right answer:
                
                            Instructions
                            ------------
                        {task_description} This is the json data: {data}                
                            Your Final answer must be correct.
  			        """),
    expected_output="A summary report with total transactionAmount along with mechBackItemCode. Don't use json format.",
    agent=transactions_assist,
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
print(f"""\n\n########################
\n## Here is the Final Result:\n
########################\n

 {final_output}
\n """)

# This is the model statistics: 
#  {final_output.model_dump_json} 