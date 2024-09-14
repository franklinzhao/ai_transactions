"""
Make sure you have boto3 1.28.57 or later. 
Prior version doesn't support bedrock as it GA couple of weeks back.'

"""

import boto3
from langchain_community.llms import Bedrock
from langchain_aws import BedrockLLM
from langchain_community.chat_models import BedrockChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from botocore.config import Config

#creating config for all required parameters to be passed to boto3.

retry_config = Config(
        region_name = 'us-east-1',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
)

# Creating boto3 session by passing profile information. Profile can be parametrized depeding upon the env you are using
session = boto3.session.Session(profile_name='default')

"""" 
btot3 provides two different client to ivoke bedrock operation.
1. bedrock : creating and managing Bedrock models.
2. bedrock-runtime : Running inference using Bedrock models.
"""
boto3_bedrock = session.client("bedrock", config=retry_config)
boto3_bedrock_runtime = session.client("bedrock-runtime", config=retry_config)


"""
Here we try to see the details of foundation models available.
Using bedrcok client you can do various model operation.
"""
print(boto3_bedrock.list_foundation_models()['modelSummaries'][0])

""" 
Here we will invoke anthropic claude model to answer a question using prompt template 
This is a inference call. We need model to generate answer for the question we provide.
Hence using bedrock-runtime module
"""
models = [
    "anthropic.claude-instant-v1",
    # "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "meta.llama3-1-70b-instruct-v1:0",
    "cohere.command-r-plus-v1:0"
]

bedrockllm = BedrockLLM(
        model_id=models[0],
        client=boto3_bedrock_runtime,
        model_kwargs={
            "temperature": 0,
            # "max_tokens_to_sample": 2048,
            # "top_p": 1,
            # "top_k": 250,
            "stop_sequences": ["\n\nHuman:"],
        },
    )

#   Define prompt template
template1 = '''I want you to act as a acting dietician for people.
In an easy way, explain the benefits of {fruit}.'''

prompt1 = PromptTemplate(
    input_variables = ['fruit'],
    template = template1
)

llm_chain = LLMChain(
    llm=bedrockllm,
    prompt=prompt1)

# print(llm_chain.run('apple'))