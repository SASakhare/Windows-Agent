# test_multitab_shopping.py
import time
from .browser_tool import BrowserTool


def run(tool: BrowserTool, action: str, **kwargs):
    """Call a tool action exactly the way the LLM/executor would,
    and print the result so we can verify each step works."""
    print(f"\n>>> execute(action={action!r}, kwargs={kwargs})")
    result = tool.execute(action, **kwargs)
    print(f"<<< result: {result}")
    return result


def main():
    tool = BrowserTool()

    # ---------------------------------------------------------
    # Amazon - search power bank
    # ---------------------------------------------------------
    run(tool, "launch", headless=False)
    amazon = run(tool, "new_tab", url="https://www.amazon.in")
    amazon_tab = amazon["tab_id"]

    run(tool, "search", query="power bank", tab_id=amazon_tab)
    run(tool, "page_state", tab_id=amazon_tab)

    # ---------------------------------------------------------
    # Flipkart - open new tab, search power bank
    # ---------------------------------------------------------
    time.sleep(5)  # wait before switching tabs
    # flipkart = run(tool, "new_tab", url="https://www.flipkart.com")
    # flipkart_tab = flipkart["tab_id"]

    # run(tool, "search", query="power bank", tab_id=flipkart_tab)
    # run(tool, "page_state", tab_id=flipkart_tab)
    run(tool, "launch", headless=False)
    amazon = run(tool, "new_tab", url="https://www.amazon.in")
    amazon_tab = amazon["tab_id"]

    run(tool, "search", query="earphone", tab_id=amazon_tab)
    run(tool, "page_state", tab_id=amazon_tab)
    # ---------------------------------------------------------
    # Myntra - open new tab, search power bank
    # ---------------------------------------------------------
    time.sleep(5)
    # myntra = run(tool, "new_tab", url="https://www.myntra.com")
    # myntra_tab = myntra["tab_id"]

    # run(tool, "search", query="power bank", tab_id=myntra_tab)
    # run(tool, "page_state", tab_id=myntra_tab)
    run(tool, "launch", headless=False)
    amazon = run(tool, "new_tab", url="https://www.amazon.in")
    amazon_tab = amazon["tab_id"]

    run(tool, "search", query="pen", tab_id=amazon_tab)
    run(tool, "page_state", tab_id=amazon_tab)
    # ------------------------------------------
    # ---------------------------------------------------------
    # Back to Amazon - search earphones, scroll for 10 seconds
    # ---------------------------------------------------------
    time.sleep(5)
    run(tool, "switch_tab", tab_id=amazon_tab)
    run(tool, "search", query="earphones", tab_id=amazon_tab)
    run(tool, "page_state", tab_id=amazon_tab)

    print("\n>>> scrolling Amazon tab for 10 seconds")
    end_time = time.time() + 10
    while time.time() < end_time:
        run(tool, "scroll", direction="down", amount=400, tab_id=amazon_tab)
        time.sleep(1)

    run(tool, "list_tabs" if False else "tabs")  # sanity check open tabs
    run(tool, "screenshot", path="amazon_earphones.png", tab_id=amazon_tab)

    input("\nPress Enter to close browser...")
    run(tool, "close")


if __name__ == "__main__":
    main()