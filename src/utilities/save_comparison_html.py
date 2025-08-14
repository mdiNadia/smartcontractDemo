# در utilities/save_results.py این بخش رو اضافه کن
def save_comparison_html(all_results, graphs_dir, output_file):
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
    display: none;
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
</style>
</head>
<body>

<h1>Smart Contract Summaries & Graphs</h1>
"""

    # ایجاد اسلایدها
    for idx, item in enumerate(all_results):
        contract_name = item["contract"]
        graph_html = os.path.join(graphs_dir, contract_name.replace(".sol", ".html"))
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
        <iframe src="graphs_view/{contract_name.replace(".sol", ".html")}"></iframe>
    </div>
</div>
"""

    # اسکریپت جاوااسکریپت برای ورق‌زدن
    html += """
<div>
    <button onclick="plusSlides(-1)">Previous</button>
    <button onclick="plusSlides(1)">Next</button>
</div>

<script>
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function showSlides(n) {
  let slides = document.getElementsByClassName("slide");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
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
