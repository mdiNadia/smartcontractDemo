from config import OUTPUT_TEXT, OUTPUT_HTML

def save_to_text(all_results, path=OUTPUT_TEXT):
    with open(path, "w", encoding="utf-8") as f:
        for r in all_results:
            f.write(f"=== {r['contract']} ===\n\n")
            f.write("Without Control-Flow:\n")
            f.write(r['no_cf'] + "\n\n")
            f.write("With Control-Flow:\n")
            f.write(r['with_cf'] + "\n\n")

def save_to_html(all_results, path=OUTPUT_HTML):
    html_content = """
    <html><head>
    <style>
    body { font-family: Arial, sans-serif; }
    .container { display: flex; gap: 20px; margin-bottom: 30px; }
    .column { width: 50%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }
    h2 { text-align: center; }
    pre { white-space: pre-wrap; }
    </style>
    </head><body>
    <h1>Smart Contract Summarization Comparison</h1>
    """
    for r in all_results:
        html_content += f"""
        <h2>{r['contract']}</h2>
        <div class="container">
            <div class="column">
                <h3>Without Control-Flow</h3>
                <pre>{r['no_cf']}</pre>
            </div>
            <div class="column">
                <h3>With Control-Flow</h3>
                <pre>{r['with_cf']}</pre>
            </div>
        </div>
        """
    html_content += "</body></html>"

    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
