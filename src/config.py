
import os

# مدل و API
OPENAI_API_KEY = ""
o_MODEL_NAME = "gpt-4o-mini"  # یا مدل دلخواه

GEMINI_API_KEY = "AIzaSyCzkzN83G_NSUB_jXlDj_HH3pVwXY2JMjs"
g_MODEL_NAME = "gemini-2.0-flash"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # مسیر پوشه src

SOLIDITY_FILE = os.path.join(BASE_DIR, "contracts", "contract.sol")
GRAPH_FILE = os.path.join(BASE_DIR, "graphs", "graph.json")
OUTPUT_TEXT = os.path.join(BASE_DIR, "client", "comparison.txt")
OUTPUT_HTML = os.path.join(BASE_DIR, "client", "comparison.html")


