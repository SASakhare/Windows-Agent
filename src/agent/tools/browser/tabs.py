# tools/browser/tabs.py
from typing import List, Dict, Any, Optional
from .browser_manager import BrowserManager


class Tabs:
    def __init__(self, manager: BrowserManager) -> None:
        self._manager = manager

    def new_tab(self, url: str = "about:blank", make_active: bool = True) -> Dict[str, Any]:
        context = self._manager.current_context
        page = context.new_page()
        url=self._normalize_url(url)
        page.goto(url)
        tab_id = self._manager.register_new_tab(page)
        if make_active:
            self._manager.set_active_tab(tab_id)
        return {"success": True, "tab_id": tab_id, "url": page.url, "title": page.title()}

    def close_tab(self, tab_id: str) -> str:
        self._manager.close_tab(tab_id)
        return f"Closed tab '{tab_id}'."

    def switch_tab(self, tab_id: str) -> Dict[str, Any]:
        page = self._manager.set_active_tab(tab_id)
        return {"success": True, "tab_id": tab_id, "url": page.url, "title": page.title()}

    def tabs(self) -> List[Dict[str, Any]]:
        return [
            {"tab_id": tid, "url": p.url, "title": p.title()}
            for tid, p in self._manager.list_tabs().items()
        ]
    
    def _normalize_url(self,url: str) -> str:

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url