# tools/browser/page.py
from typing import Dict, Any, List, Optional
from .browser_manager import BrowserManager


class Page:
    """Reads page content/state. No navigation, no clicking."""

    def __init__(self, manager: BrowserManager) -> None:
        self._manager = manager

    def html(self, tab_id: Optional[str] = None) -> str:
        return self._manager.get_page(tab_id).content()

    def text(self, tab_id: Optional[str] = None) -> str:
        return self._manager.get_page(tab_id).inner_text("body")

    def screenshot(self, path: str = "screenshot.png", tab_id: Optional[str] = None) -> str:
        self._manager.get_page(tab_id).screenshot(path=path)
        return path

    def buttons(self, tab_id: Optional[str] = None) -> List[str]:
        page = self._manager.get_page(tab_id)
        return [b.strip() for b in page.get_by_role("button").all_inner_texts() if b.strip()]

    def links(self, tab_id: Optional[str] = None) -> List[str]:
        page = self._manager.get_page(tab_id)
        return [a.strip() for a in page.get_by_role("link").all_inner_texts() if a.strip()]

    def textboxes(self, tab_id: Optional[str] = None) -> List[str]:
        page = self._manager.get_page(tab_id)
        boxes = page.get_by_role("textbox")
        names = []
        for i in range(boxes.count()):
            name = boxes.nth(i).get_attribute("aria-label") or boxes.nth(i).get_attribute("placeholder") or ""
            if name:
                names.append(name.strip())
        return names

    def page_state(self, tab_id: Optional[str] = None) -> Dict[str, Any]:
        page = self._manager.get_page(tab_id)
        resolved_id = tab_id or self._manager.get_tab_id(page)
        return {
            "tab_id": resolved_id,
            "url": page.url,
            "title": page.title(),
            "buttons": self.buttons(tab_id)[:20],
            "links": self.links(tab_id)[:20],
            "textboxes": self.textboxes(tab_id)[:20],
        }