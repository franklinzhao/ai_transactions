from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from llama_index.llms.fireworks import Fireworks
import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

nvidia_hosted_llm = ChatNVIDIA(
  # model="ai-llama-3_1-405b-instruct",
  # model="ai-llama-3_1-405b-instruct",
  # model="ai-phi-3_5-moe",
  model="ai-gemma-2-27b-it",
  api_key=os.environ["NVIDIA_API_KEY"],
  temperature=0.2,
  top_p=0.7,
  max_tokens=4096,
)

 # get a free key at https://fireworks.ai/api-keys

groq_hosted_llm = ChatGroq(
    model="llama-3.1-70b-versatile", #gemma2-9b-it
    # model="whisper-large-v3", #gemma2-9b-it
    # model="llama-3.1-8b-instant", #gemma2-9b-it
    temperature=0.5,
    max_tokens=1024,
    stop=None,
)

firework_hosted_llm = Fireworks(model="accounts/fireworks/models/llama-v3p1-405b-instruct", temperature=0)# localllm = Ollama(model="codestral:latest")#llama3.1:8b 
local_llama8b_llm = Ollama(model="llama3.1:8b")#llama3.1:8b 

# def llm_list():
#     llms=[]
#     llms.append(groq_hosted_llama,firework_hosted_llama,llama8b_local, nvidia_llm)
#     return llms