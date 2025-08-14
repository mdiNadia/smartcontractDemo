PROMPT_NO_CF_TMPL = """You are a blockchain security auditor.
Summarize the following Solidity smart contract:
---
{code}
---
Provide:
- Main purpose
- Key functions
- Potential security considerations
"""

PROMPT_WITH_CF_TMPL = """You are a blockchain security auditor.
Use the following control-flow steps to guide your analysis, then summarize the Solidity contract.
Control Flow Steps:
{steps}

Contract code:
---
{code}
---
Provide:
- Main purpose
- Key functions and their relationships
- Potential security considerations (be specific)
"""

def build_prompt_no_cf(code):
    return PROMPT_NO_CF_TMPL.format(code=code)

def build_prompt_with_cf(code, steps):
    return PROMPT_WITH_CF_TMPL.format(code=code, steps="\n".join(steps))
