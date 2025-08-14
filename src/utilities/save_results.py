from config import OUTPUT_TEXT, OUTPUT_HTML

def save_as_text(summary_no_cf: str, summary_with_cf: str):
    with open(OUTPUT_TEXT, "w", encoding="utf-8") as f:
        f.write("=== Summary WITHOUT Control-Flow ===\n\n")
        f.write(summary_no_cf + "\n\n")
        f.write("=== Summary WITH Control-Flow ===\n\n")
        f.write(summary_with_cf + "\n")

def save_as_html(summary_no_cf: str, summary_with_cf: str):
    html_content = f"""
    <html>
    <head>
    <style>
    body {{ font-family: Arial, sans-serif; }}
    .container {{ display: flex; gap: 20px; }}
    .column {{ width: 50%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }}
    h2 {{ text-align: center; }}
    pre {{ white-space: pre-wrap; }}
    </style>
    </head>
    <body>
    <h1>Smart Contract Summarization Comparison</h1>
    <div class="container">
        <div class="column">
            <h2>Without Control-Flow</h2>
            <pre>{summary_no_cf}</pre>
        </div>
        <div class="column">
            <h2>With Control-Flow</h2>
            <pre>{summary_with_cf}</pre>
        </div>
    </div>
    </body>
    </html>
    """
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
