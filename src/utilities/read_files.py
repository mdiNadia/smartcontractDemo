import json
from config import SOLIDITY_FILE, GRAPH_FILE

def read_solidity_code():
    with open(SOLIDITY_FILE, "r", encoding="utf-8") as f:
        return f.read()

def read_control_flow_graph():
    with open(GRAPH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# # craete prompts
# prompt_no_cf = f"""You are a blockchain security auditor. 
# Summarize the following Solidity smart contract:
# {solidity_code}
# """

# prompt_with_cf = f"""You are a blockchain security auditor. 
# Summarize the following Solidity smart contract.
# Here is the control-flow graph in JSON format:
# {json.dumps(control_flow_graph, indent=2)}
# Then, provide a concise summary including:
# - Main purpose of the contract
# - Key functions and their relationships
# - Potential security considerations
# Contract code:
# {solidity_code}
# """
# #ارسال هر دو پرامپت به مدل زبانی
# from openai import OpenAI
# client = OpenAI(api_key="YOUR_API_KEY")

# def get_summary(prompt):
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",  # یا هر مدلی که انتخاب می‌کنی
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content.strip()

# summary_no_cf = get_summary(prompt_no_cf)
# summary_with_cf = get_summary(prompt_with_cf)
