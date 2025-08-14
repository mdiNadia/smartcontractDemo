# src/main.py
import os
import subprocess
from config import CONTRACTS_DIR, GRAPHS_DIR, GRAPH_STEPS_DIR, CLIENT_DIR
from utilities.helpers import ensure_dirs
from utilities.read_files import read_contract
from utilities.prompts import build_prompt_no_cf, build_prompt_with_cf
from utilities.llm_client import get_summary
from utilities.save_results import save_to_text, save_to_html
# --- مسیرهای اضافی ---
GRAPHS_VIEW_DIR = os.path.join(CLIENT_DIR, "graphs_view")
ensure_dirs(GRAPHS_DIR, GRAPH_STEPS_DIR, CLIENT_DIR, GRAPHS_VIEW_DIR)

# --- مسیر JS ها ---
EXTRACT_GRAPH_JS = os.path.join(os.path.dirname(__file__), "utilities", "extract_graph.js")
GRAPH_TO_STEPS_JS = os.path.join(os.path.dirname(__file__), "utilities", "graph_to_steps.js")

# --- تابع ذخیره HTML تعاملی گراف ---
import shutil

def save_graph_html(graph_file, html_file):
    # کپی JSON کنار HTML
    json_target = os.path.join(os.path.dirname(html_file), os.path.basename(graph_file))
    shutil.copyfile(graph_file, json_target)

    html_template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Graph Visualization - {os.path.basename(html_file)}</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
body {{ background: #111; color: white; }}
.link {{ stroke: #888; stroke-width: 2px; }}
.node circle {{ stroke: #fff; stroke-width: 1.5px; }}
text {{ fill: white; font-size: 12px; }}
</style>
</head>
<body>
<h1 style="text-align:center">{os.path.basename(html_file)}</h1>
<svg width="1000" height="1100"></svg>
<script>
const svg = d3.select("svg");
const width = +svg.attr("width");
const height = +svg.attr("height");
d3.json("{os.path.basename(graph_file)}").then(data => {{
  const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.edges || data.links).id(d => d.id).distance(120))
    .force("charge", d3.forceManyBody().strength(-400))
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svg.append("g")
    .selectAll("line")
    .data(data.edges || data.links)
    .join("line")
    .attr("class", "link");

  const node = svg.append("g")
    .selectAll("circle")
    .data(data.nodes)
    .join("circle")
    .attr("r", 8)
    .attr("fill", d => d.external ? "orange" : "steelblue")
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended)
    );

  const label = svg.append("g")
    .selectAll("text")
    .data(data.nodes)
    .join("text")
    .text(d => d.id);

  simulation.on("tick", () => {{
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);

    label
      .attr("x", d => d.x + 10)
      .attr("y", d => d.y + 3);
  }});

  function dragstarted(event) {{
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }}
  function dragged(event) {{
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }}
  function dragended(event) {{
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }}
}});
</script>
</body>
</html>"""
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_template)
# در utilities/save_results.py این بخش رو اضافه کن
def comparison_html(all_results, graphs_dir, output_file):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Contracts Comparison</title>
<style>
body {
    background: #111;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
}
.slide {
    display: none; /* پیش‌فرض مخفی */
}
h2 { color: #0af; }
button {
    background: #0af;
    color: white;
    padding: 10px 20px;
    margin: 20px;
    border: none;
    cursor: pointer;
    border-radius: 5px;
}
button:hover { background: #09c; }
.content-box {
    background: #222;
    padding: 15px;
    margin: 15px auto;
    border-radius: 8px;
    width: 80%;
    text-align: left;
}
iframe {
    width: 90%;
    height: 400px;
    border: none;
    border-radius: 5px;
    margin-top: 10px;
}
pre {
    white-space: pre-wrap;   
    word-wrap: break-word;
    overflow-wrap: break-word;
}
</style>
</head>
<body>

<h1>Smart Contract Summaries & Graphs</h1>
"""

    for idx, item in enumerate(all_results):
        contract_name = item["contract"]
        html += f"""
<div class="slide">
    <h2>{contract_name}</h2>
    <div class="content-box">
        <h3>Without Control-Flow</h3>
        <pre>{item["no_cf"]}</pre>
    </div>
    <div class="content-box">
        <h3>With Control-Flow</h3>
        <pre>{item["with_cf"]}</pre>
    </div>
    <div class="content-box">
        <h3>Interactive Graph</h3>
        <iframe src="graphs_view/{contract_name.replace('.sol', '.html')}"></iframe>
    </div>
</div>
"""

    html += """
<div>
    <button onclick="plusSlides(-1)">Previous</button>
    <button onclick="plusSlides(1)">Next</button>
</div>

<script>
let slideIndex = 1;

window.onload = function() {
    showSlides(slideIndex);
}

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function showSlides(n) {
  let slides = document.getElementsByClassName("slide");
  if (n > slides.length) { slideIndex = 1 }
  if (n < 1) { slideIndex = slides.length }
  for (let i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}
</script>

</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

# --- پردازش یک قرارداد ---
def process_contract(contract_path, graph_path, steps_path):
    code = read_contract(contract_path)

    # استخراج گراف با Node.js
    subprocess.run(["node", EXTRACT_GRAPH_JS, contract_path, graph_path], check=True)

    # استخراج مراحل از گراف
    subprocess.run(["node", GRAPH_TO_STEPS_JS, graph_path, steps_path], check=True)
    with open(steps_path, "r", encoding="utf-8") as f:
        steps = [line.strip() for line in f.readlines()]

    # ساخت پرامپت‌ها
    prompt_no_cf = build_prompt_no_cf(code)
    prompt_with_cf = build_prompt_with_cf(code, steps)

    # گرفتن خلاصه‌ها
    summary_no_cf = get_summary(prompt_no_cf)
    summary_with_cf = get_summary(prompt_with_cf)

    return summary_no_cf, summary_with_cf

# --- پردازش همه قراردادها ---
all_results = []

sol_files = [f for f in os.listdir(CONTRACTS_DIR) if f.endswith(".sol")]
sol_files.sort()

for f in sol_files:
    contract_path = os.path.join(CONTRACTS_DIR, f)
    graph_file = os.path.join(GRAPHS_DIR, f.replace(".sol", ".json"))
    steps_file = os.path.join(GRAPH_STEPS_DIR, f.replace(".sol", ".txt"))
    html_graph_file = os.path.join(GRAPHS_VIEW_DIR, f.replace(".sol", ".html"))

    print(f"Processing {f} ...")
    summary_no_cf, summary_with_cf = process_contract(contract_path, graph_file, steps_file)

    # ذخیره HTML تعاملی گراف
    save_graph_html(graph_file, html_graph_file)
    print(f"Saved interactive graph: {html_graph_file}")

    all_results.append({
        "contract": f,
        "no_cf": summary_no_cf,
        "with_cf": summary_with_cf
    })

# --- ذخیره خروجی مقایسه ---
save_to_text(all_results)
save_to_html(all_results)
comparison_file = os.path.join(CLIENT_DIR, "comparison.html")
comparison_html(all_results, "graphs_view", comparison_file)
print("All comparison results saved successfully.")

# --- ساخت داشبورد مرکزی ---
dashboard_file = os.path.join(CLIENT_DIR, "graphs_dashboard.html")
graph_html_files = [f for f in os.listdir(GRAPHS_VIEW_DIR) if f.endswith(".html")]
graph_html_files.sort()

dashboard_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Smart Contract Graph Dashboard</title>
<style>
body { background: #111; color: white; font-family: Arial, sans-serif; }
h1 { text-align: center; }
.container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
.card { background: #222; border-radius: 8px; padding: 10px; width: 300px; text-align: center; }
.card a { color: #0af; text-decoration: none; font-weight: bold; }
iframe { width: 100%; height: 300px; border: none; border-radius: 5px; }
pre {
    white-space: pre-wrap;     
    word-wrap: break-word;  
    overflow-wrap: break-word; 
}
</style>
</head>
<body>
<h1>Smart Contract Graph Dashboard</h1>
<div class="container">
"""

for g in graph_html_files:
    path = os.path.join("graphs_view", g)
    dashboard_html += f"""
<div class="card">
    <a href="{path}" target="_blank">{g}</a>
    <iframe src="{path}"></iframe>
</div>
"""

dashboard_html += """
</div>
</body>
</html>
"""

with open(dashboard_file, "w", encoding="utf-8") as f:
    f.write(dashboard_html)

print(f"Dashboard created: {dashboard_file}")
