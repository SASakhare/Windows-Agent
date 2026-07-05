# tools/browser/navigation.py
from typing import Dict, Any, Optional
from .browser_manager import BrowserManager


class Navigation:
    """Handles moving around websites. No clicking, no reading content."""

    def __init__(self, manager: BrowserManager) -> None:
        self._manager = manager

    def goto(self, url: str, tab_id: Optional[str] = None, timeout: float = 30000) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.goto(url, timeout=timeout)
        return self._result(page, tab_id)

    def back(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.go_back()
        return self._result(page, tab_id)

    def forward(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.go_forward()
        return self._result(page, tab_id)

    def reload(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        page.reload()
        return self._result(page, tab_id)

    def current_url(self, tab_id: Optional[str] = None) -> str:
        return self._manager.get_page(tab_id).url

    def title(self, tab_id: Optional[str] = None) -> str:
        return self._manager.get_page(tab_id).title()

    def _result(self, page, tab_id: Optional[str]) -> Dict[str, Any]:
        resolved_id = tab_id or self._manager.get_tab_id(page)
        return {"success": True, "tab_id": resolved_id, "url": page.url, "title": page.title()}