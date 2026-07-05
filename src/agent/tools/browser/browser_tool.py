# tools/browser/browser_tool.py
from typing import Any, Dict, List, Optional

from src.agent.tools.base_tool import BaseTool
from .browser_manager import BrowserManager
from .navigation import Navigation
from .interaction import Interaction
from .page import Page
from .tabs import Tabs


class BrowserTool(BaseTool):
    """Control a web browser: navigate, click, type, search, read page state.

    Internally delegates to BrowserManager, Navigation, Interaction, Page,
    and Tabs, but every action below is exposed directly on this class so
    it can be introspected and turned into a schema automatically.
    """

    def __init__(self) -> None:
        self.manager = BrowserManager()
        self.navigation = Navigation(self.manager)
        self.interaction = Interaction(self.manager)
        self.page = Page(self.manager)
        self.tabs = Tabs(self.manager)

    @property
    def name(self) -> str:
        return "browser"

    @property
    def description(self) -> str:
        return "Control a web browser: navigate, click, type, search, read page state."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "launch": self.launch,
            "close": self.close,
            "goto": self.goto,
            "back": self.back,
            "forward": self.forward,
            "reload": self.reload,
            "click_button": self.click_button,
            "click_link": self.click_link,
            "fill_textbox": self.fill_textbox,
            "search": self.search,
            "press_enter": self.press_enter,
            "press_escape": self.press_escape,
            "page_state": self.page_state,
            "html": self.html,
            "screenshot": self.screenshot,
            "new_tab": self.new_tab,
            "close_tab": self.close_tab,
            "switch_tab": self.switch_tab,
            "tabs": self.list_tabs,
            "scroll": self.scroll,
        }

        if action not in actions:
            raise ValueError(f"Unknown action: {action}")

        if action != "launch" and not self.manager.is_open():
            self.launch()

        return actions[action](**kwargs)

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def launch(self, headless: bool = False) -> str:
        """Launch the browser. Called automatically by other actions if
        the browser isn't open yet; rarely needs to be called directly.

        Args:
            headless: Run without a visible window.

        Returns:
            Status message.
        """
        return self.manager.launch(headless=headless)

    def close(self) -> str:
        """Close the browser and end the session.

        Returns:
            Status message.
        """
        return self.manager.close()

    # ==========================================================
    # Navigation
    # ==========================================================

    def goto(self, url: str, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Navigate the active (or specified) tab to a URL.

        Args:
            url: The URL to navigate to.
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title after navigation.
        """
        return self.navigation.goto(url, tab_id=tab_id) 

    def back(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Go back one page in browser history.

        Args:
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title after navigation.
        """
        return self.navigation.back(tab_id=tab_id) 

    def forward(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Go forward one page in browser history.

        Args:
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title after navigation.
        """
        return self.navigation.forward(tab_id=tab_id)

    def reload(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Reload the current page.

        Args:
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title after reload.
        """
        return self.navigation.reload(tab_id=tab_id)

    # ==========================================================
    # Interaction
    # ==========================================================

    def click_button(self, name: str, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Click a button identified by its visible/accessible name.
        Use the button's visible text, not a CSS selector, e.g.
        click_button(name="Login").

        Args:
            name: Visible name/text of the button.
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title after the click.
        """
        return self.interaction.click_button(name, tab_id=tab_id) 

    def click_link(self, name: str, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Click a link identified by its visible text.

        Args:
            name: Visible text of the link.
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title after the click.
        """
        return self.interaction.click_link(name, tab_id=tab_id)

    def fill_textbox(self, name: str, text: str, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Type text into an input field identified by its label or
        placeholder, e.g. fill_textbox(name="Username", text="sejal").

        Args:
            name: Label/placeholder of the textbox.
            text: Text to type into it.
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title after filling.
        """
        return self.interaction.fill_textbox(name, text, tab_id=tab_id)

    def search(self, query: str, textbox_name: Optional[str] = None, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Fill the page's search box with a query and press Enter.

        Args:
            query: Search text to submit.
            textbox_name: Optional explicit name of the search box, if
                the page has more than one textbox.
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title after searching.
        """
        return self.interaction.search(query, textbox_name=textbox_name, tab_id=tab_id)

    def press_enter(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Press the Enter key on the active element.

        Args:
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title.
        """
        return self.interaction.press_enter(tab_id=tab_id)

    def press_escape(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Press the Escape key on the active element.

        Args:
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title.
        """
        return self.interaction.press_escape(tab_id=tab_id)

    # ==========================================================
    # Page observation
    # ==========================================================

    def page_state(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a compact snapshot of the page: title, url, visible
        buttons, links, and textboxes. Call this after any action to
        see what changed, instead of requesting full HTML.

        Args:
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with url, title, buttons, links, textboxes.
        """
        return self.page.page_state(tab_id=tab_id)

    def html(self, tab_id: Optional[str] = None) -> str:
        """Get raw HTML of the page. Expensive - only use if
        page_state() doesn't have enough info to find an element.

        Args:
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Raw HTML string.
        """
        return self.page.html(tab_id=tab_id)

    def screenshot(self, path: str = "screenshot.png", tab_id: Optional[str] = None) -> str:
        """Take a screenshot of the page and save it to disk.

        Args:
            path: File path to save the screenshot to.
            tab_id: Target a specific tab instead of the active one.

        Returns:
            The file path the screenshot was saved to.
        """
        return self.page.screenshot(path=path, tab_id=tab_id)

    # ==========================================================
    # Tabs
    # ==========================================================

    def new_tab(self, url: str = "about:blank", make_active: bool = True) -> Dict[str, Any]:
        """Open a new browser tab, optionally navigating to a URL.
        Returns a tab_id that can be passed to other actions to target
        this tab directly without switching.

        Args:
            url: URL to load in the new tab.
            make_active: Whether to make this the active tab.

        Returns:
            Dictionary with success, tab_id, and url.
        """
        return self.tabs.new_tab(url=url, make_active=make_active)

    def switch_tab(self, tab_id: str) -> Dict[str, Any]:
        """Make a given tab the active tab. Only needed if you're not
        passing tab_id explicitly to other actions.

        Args:
            tab_id: The tab to switch to.

        Returns:
            Dictionary with success, url, and title of the switched-to tab.
        """
        return self.tabs.switch_tab(tab_id)

    def close_tab(self, tab_id: str) -> str:
        """Close a tab by its tab_id.

        Args:
            tab_id: The tab to close.

        Returns:
            Status message.
        """
        return self.tabs.close_tab(tab_id)

    def list_tabs(self) -> List[Dict[str, Any]]:
        """List all open tabs with their tab_id, url, and title.

        Returns:
            List of dictionaries, one per open tab.
        """
        return self.tabs.tabs()
    
    def scroll(self, direction: str = "down", amount: int = 800, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Scroll the page up or down by a pixel amount.

        Args:
            direction: "down" or "up".
            amount: Pixels to scroll.
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title.
        """
        return self.interaction.scroll(direction=direction, amount=amount, tab_id=tab_id)

import time


if __name__ == "__main__":
    tool = BrowserTool()
    tool.execute("goto", url="https://google.com")
    print(tool.execute("page_state"))

    time.sleep(30)
    tool.execute("close")