from autogen import ConversableAgent, AssistantAgent
import llms
# https://github.com/tylerprogramming/autogen-beginner-course.git+
def create_llm_config(model, base_url,api_key, temperature, seed):
    config_list = [
        {
            "model": model,
            "base_url": base_url,
            "api_key": api_key,
        },
    ]
    llm_config = {
        "seed": int(seed),
        "config_list": config_list,
        "temperature": float(temperature),
    }
    return llm_config

model= "llama-3.1-70b-versatile"
base_url="https://api.groq.com/openai/v1"
api_key= "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"

llm = create_llm_config(model,base_url,api_key,temperature="0.7",seed=0)

emma = AssistantAgent(
    "emma", llm_config=llm, system_message="you are a helpful joker evaluator."
)
jack = ConversableAgent(
    "jack", llm_config=llm, system_message="you are a helpful joker."
)

chat_result = emma.initiate_chat(jack,message="please give me a joke.",max_turns=2)