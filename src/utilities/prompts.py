import json

def create_prompt_no_cf(solidity_code: str) -> str:
    return f"""You are a blockchain security auditor.
Summarize the following Solidity smart contract:
{solidity_code}
"""

def create_prompt_with_cf(solidity_code: str, control_flow_graph: dict) -> str:
    return f"""You are a blockchain security auditor.
Summarize the following Solidity smart contract.
Here is the control-flow graph in JSON format:
{json.dumps(control_flow_graph, indent=2)}
Then, provide a concise summary including:
- Main purpose of the contract
- Key functions and their relationships
- Potential security considerations
Contract code:
{solidity_code}
"""
