""" 
Sample Project Description:
project 1. 
I want to build a snake game, the snake will grow in length after it eat foods. the player use arrow to control its movement. 
the objective is not to crash to walls,otherwise the player will lose. press q to quit the game. press s to stop the game. 

"""

import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process
import random
import os
from customtools import decimalremove_sum_tool, duckduckgo_search, internet_search_tool
from dotenv import load_dotenv
import llms 
load_dotenv()

llm = llms.nvidia_hosted_llm

# Get user inputs
# project_name = input("Please provide a project name, no space and length is within 10 characters.\n")
project_description = input("What is the program you would like to build? Please provide detailed description of the program and its requirements.\n")
# code_language = input("what's the language of coding?")

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
tax_accountant = Agent(
    llm=llm,
    role='tax accountant',
    goal='calculate the correct number',
    backstory=dedent("""Instructions
                        You are a tax accountant at a tax reporting firm.
                        Your expertise in tax calculation. and do your best to
                        produce the correct answer; you can use tools specified. """),
    allow_delegation=False,
    verbose=True,
    tools=[decimalremove_sum_tool,internet_search_tool],
    # tools=[decimalremove_sum_tool(result_as_answer=True)],
    memory=True,
    # function_calling_llm=firework_hosted_llama,
    tools_results=[],
    max_iter=50 
)

# Define task
tool_use_task = Task(
    llm=llm,
    description=dedent(f"""You will be give two numbers and use the tools to get the right answer:
                
                            Instructions
                            ------------
                        {project_description}
                
                            Your Final answer must be correct out put by using the tool.
  			        """),
    expected_output="A result by using the tool.",
    agent=tax_accountant,
    tools=[decimalremove_sum_tool,duckduckgo_search],
    human_input=True
)

# Define the team
crew = Crew(
  agents=[tax_accountant],
  tasks=[tool_use_task],
  verbose=True,
#   embedder={
#             "provider": "google",
#             "config":{
#                 "model": 'models/embedding-001',
#                 "task_type": "retrieval_document",
#                 "title": "Embeddings for Embedchain"
#             }
#         }        
)

# The team to start work
final_output = crew.kickoff()

# Print output
print(f"""\n\n########################
\n## Here is the final output of result
########################\n
final code for the project:
 {final_output}

This is the model statistics: 
 {final_output.model_dump_json}
 """)

#save it to local folder



