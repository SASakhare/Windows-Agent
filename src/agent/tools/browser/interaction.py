# tools/browser/interaction.py
from typing import Dict, Any, Optional
from .browser_manager import BrowserManager


class Interaction:
    """User-intent actions: click_button('Login'), not click(css_selector)."""

    def __init__(self, manager: BrowserManager) -> None:
        self._manager = manager

    def click_button(self, name: str, tab_id: Optional[str] = None, timeout: float = 5000) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.get_by_role("button", name=name).click(timeout=timeout)
        return self._result(page, tab_id)

    def click_link(self, name: str, tab_id: Optional[str] = None, timeout: float = 5000) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.get_by_role("link", name=name).click(timeout=timeout)
        return self._result(page, tab_id)

    def fill_textbox(self, name: str, text: str, tab_id: Optional[str] = None, timeout: float = 5000) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.get_by_role("textbox", name=name).fill(text, timeout=timeout)
        return self._result(page, tab_id)

    def search(self, query: str, textbox_name: Optional[str] = None, tab_id: Optional[str] = None) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        locator = (
            page.get_by_role("searchbox")
            if textbox_name is None
            else page.get_by_role("textbox", name=textbox_name)
        )
        locator.fill(query)
        locator.press("Enter")
        return self._result(page, tab_id)

    def press_enter(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.keyboard.press("Enter")
        return self._result(page, tab_id)

    def press_escape(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.keyboard.press("Escape")
        return self._result(page, tab_id)
    
    def scroll(self, direction: str = "down", amount: int = 800, tab_id: Optional[str] = None) -> Dict[str, Any]:
        """Scroll the page up or down by a pixel amount.

        Args:
            direction: "down" or "up".
            amount: Pixels to scroll.
            tab_id: Target a specific tab instead of the active one.

        Returns:
            Dictionary with success, url, and title.
        """
        page = self._manager.get_page(tab_id)
        delta = amount if direction == "down" else -amount
        page.mouse.wheel(0, delta)
        return self._result(page, tab_id)

    def _result(self, page, tab_id: Optional[str]) -> Dict[str, Any]:
        resolved_id = tab_id or self._manager.get_tab_id(page)
        return {"success": True, "tab_id": resolved_id, "url": page.url, "title": page.title()}