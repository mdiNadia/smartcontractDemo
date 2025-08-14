import json

def read_contract(contract_path):
    with open(contract_path, "r", encoding="utf-8") as f:
        return f.read()

def read_graph(graph_path):
    with open(graph_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_steps(steps, steps_path):
    with open(steps_path, "w", encoding="utf-8") as f:
        f.write("\n".join(steps))
