
from utilities.read_files import read_solidity_code, read_control_flow_graph
from utilities.prompts import create_prompt_no_cf, create_prompt_with_cf
from utilities.llm_client import get_summary
from utilities.save_results import save_as_text, save_as_html

def main():
    # 1. خواندن داده‌ها
    solidity_code = read_solidity_code()
    control_flow_graph = read_control_flow_graph()

    # 2. ساخت پرامپت‌ها
    prompt_no_cf = create_prompt_no_cf(solidity_code)
    prompt_with_cf = create_prompt_with_cf(solidity_code, control_flow_graph)

    # 3. ارسال به LLM
    summary_no_cf = get_summary(prompt_no_cf)
    summary_with_cf = get_summary(prompt_with_cf)

    # 4. ذخیره خروجی
    save_as_text(summary_no_cf, summary_with_cf)
    save_as_html(summary_no_cf, summary_with_cf)

    print(" Summarization completed! Check comparison.txt and comparison.html.")

if __name__ == "__main__":
    main()
