PROMPT_NO_CF_TMPL = """You are a professional blockchain security auditor.
Analyze the following Solidity smart contract carefully. Focus only on what is explicitly in the code. 
Do not include any Markdown symbols or formatting.

Contract code:
---
{code}
---

Provide the following:

1. Main purpose of the contract (concise, 1-2 sentences)
2. Key functions and their exact roles
3. Any potential security considerations or vulnerabilities that are directly observable from the code
4. Relationships between functions affecting security

Output in plain text, structured and clear. Avoid speculation.
"""

PROMPT_WITH_CF_TMPL = """You are a professional blockchain security auditor.
Use the following control-flow steps to guide your analysis, then summarize the Solidity contract.
Focus only on what is explicitly in the code and control-flow. Do not include any Markdown symbols or formatting.

Control Flow Steps:
{steps}

Contract code:
---
{code}
---

Provide the following:

1. Main purpose of the contract (concise, 1-2 sentences)
2. Key functions, their exact roles, and relationships considering control flow
3. Any potential security considerations or vulnerabilities observable from the code and control flow

Output in plain text, structured and clear. Avoid speculation.
"""

def build_prompt_no_cf(code):
    return PROMPT_NO_CF_TMPL.format(code=code)

def build_prompt_with_cf(code, steps):
    return PROMPT_WITH_CF_TMPL.format(code=code, steps="\n".join(steps))
