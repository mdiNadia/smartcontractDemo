import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# مسیرها
CONTRACTS_DIR = os.path.join(BASE_DIR, "contracts")
GRAPHS_DIR = os.path.join(BASE_DIR, "graphs")
GRAPH_STEPS_DIR = os.path.join(BASE_DIR, "graph_steps")
CLIENT_DIR = os.path.join(BASE_DIR, "client")

OUTPUT_TEXT = os.path.join(CLIENT_DIR, "comparison.txt")
OUTPUT_HTML = os.path.join(CLIENT_DIR, "comparison.html")

# LLM Config
GEMINI_API_KEY = "AIzaSyAtJFTn3nUn-UlPq0NayS0wNOAxhBHG09M"
G_MODEL_NAME = "gemini-2.0-flash"
# مدل و API
OPENAI_API_KEY = ""
O_MODEL_NAME = "gpt-4o-mini"  # یا مدل دلخواه





