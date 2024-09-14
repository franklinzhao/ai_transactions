from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from llama_index.llms.fireworks import Fireworks
import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import boto3
from langchain_aws import BedrockLLM
from langchain_community.chat_models import BedrockChat
from langchain_cohere.llms import Cohere, BaseCohere
import cohere


load_dotenv()

nvidia_hosted_llm = ChatNVIDIA(
  model="meta/llama-3.1-405b-instruct",
  # model="microsoft/phi-3.5-moe-instruct",
  # model="ai-phi-3_5-moe",
  # model="ai21labs/jamba-1.5-large-instruct", #based on mamba, support 256k long context window
  # model="ai-gemma-2-27b-it",
  api_key=os.environ["NVIDIA_API_KEY"],
  temperature=0.1,
  top_p=0.7,
  max_tokens=40960,
)

 # get a free key at https://fireworks.ai/api-keys

groq_hosted_llm = ChatGroq(
    model="llama-3.1-70b-versatile", #gemma2-9b-it
    # model="whisper-large-v3", #gemma2-9b-it
    # model="llama-3.1-8b-instant", #gemma2-9b-it
    temperature=0.5,
    max_tokens=8000,
    stop=None,
)

# Toronto based model
# baseCohere = BaseCohere(cohere_api_key=os.environ["COHERE_API_KEY"], model="command-r-plus-08-2024", temperature=0.5)
# llm_cohere = Cohere(BaseCohere)
# cohereclient =cohere.client(cohere_api_key=os.environ["COHERE_API_KEY"])
# model="command-r-plus-08-2024",
llm_cohere = Cohere(cohere_api_key=os.environ["COHERE_API_KEY"],  temperature=0.5, max_tokens=128000)

firework_hosted_llm = Fireworks(model="accounts/fireworks/models/llama-v3p1-405b-instruct", temperature=0)# localllm = Ollama(model="codestral:latest")#llama3.1:8b 
local_llama8b_llm = Ollama(model="llama3.1:8b")#llama3.1:8b 

#AWS bedrock hosted llm
# retry_config = Config(
#         region_name = 'us-east-1',
#         retries = {
#             'max_attempts': 10,
#             'mode': 'standard'
#         }
# )
# session = boto3.session.Session(profile_name='default')
# boto3_bedrock = session.client("bedrock", config=retry_config)
# boto3_bedrock_runtime = session.client("bedrock-runtime", config=retry_config)

bedrock_models = [
    "anthropic.claude-instant-v1",
    # "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "meta.llama3-1-70b-instruct-v1:0",
    "cohere.command-r-plus-v1:0"
]

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
bedrock_llm1 = BedrockLLM(
    client=bedrock_client, 
    model_id='cohere.command-r-plus-v1:0'  # Replace with a valid model ID from Bedrock
)

bedrock_llm = BedrockLLM(
    credentials_profile_name="default",
    model_id=bedrock_models[0],  # ARN like 'arn:aws:bedrock:...' obtained via provisioning the custom model
    model_kwargs={"temperature": 0.7},
    # streaming=True,
)

bedrock_llm.invoke(input="What is the recipe of mayonnaise?")
