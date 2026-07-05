# tools/browser/browser_manager.py
import itertools
from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page


class BrowserManager:
    """Owns the Playwright lifecycle: browser, context, active page, and
    a registry of all open tabs addressable by tab_id.

    All other browser modules (Navigation, Interaction, Page, Tabs) must
    go through get_page(tab_id) instead of caching their own page
    reference, so tab switches/new tabs/closures are always reflected
    correctly everywhere.
    """

    def __init__(self) -> None:
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

        self._tabs: Dict[str, Page] = {}
        self._id_counter = itertools.count(1)

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def launch(self, headless: bool = False) -> str:
        if self._browser:
            return "Browser already launched."

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=headless)
        self._context = self._browser.new_context()
        page = self._context.new_page()
        self._page = page
        self._register_tab(page)
        return "Browser launched."

    def close(self) -> str:
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        self._browser = self._context = self._page = None
        self._playwright = None
        self._tabs.clear()
        return "Browser closed."

    def is_open(self) -> bool:
        return self._browser is not None

    def browser_info(self) -> Dict[str, Any]:
        if not self._browser:
            return {"open": False}
        return {
            "open": True,
            "is_connected": self._browser.is_connected(),
            "num_tabs": len(self._tabs),
        }

    # ---------------------------------------------------------
    # Tab registry
    # ---------------------------------------------------------

    def _register_tab(self, page: Page) -> str:
        tab_id = f"tab-{next(self._id_counter)}"
        self._tabs[tab_id] = page
        page.on("close", lambda: self._on_tab_closed(tab_id)) # type: ignore
        return tab_id

    def _on_tab_closed(self, tab_id: str) -> None:
        self._tabs.pop(tab_id, None)
        if self._page and self._tab_id_for_page(self._page) is None:
            # Active page was closed - fall back to any remaining tab.
            remaining = list(self._tabs.values())
            self._page = remaining[-1] if remaining else None

    def _tab_id_for_page(self, page: Page) -> Optional[str]:
        for tid, p in self._tabs.items():
            if p == page:
                return tid
        return None

    def register_new_tab(self, page: Page) -> str:
        """Called by Tabs.new_tab() after creating a page."""
        return self._register_tab(page)

    def get_page(self, tab_id: Optional[str] = None) -> Page:
        """Return the page for tab_id, or the active page if tab_id is None."""
        self._require_open()
        if tab_id is None:
            if self._page is None:
                raise RuntimeError("No active tab.")
            return self._page
        if tab_id not in self._tabs:
            raise ValueError(f"No such tab_id: '{tab_id}'. Open tabs: {list(self._tabs.keys())}")
        return self._tabs[tab_id]

    def get_tab_id(self, page: Page) -> Optional[str]:
        return self._tab_id_for_page(page)

    def list_tabs(self) -> Dict[str, Page]:
        return dict(self._tabs)

    def set_active_tab(self, tab_id: str) -> Page:
        page = self.get_page(tab_id)
        self._page = page
        return page

    def close_tab(self, tab_id: str) -> None:
        page = self.get_page(tab_id)
        page.close()  # triggers _on_tab_closed via the "close" event

    # ---------------------------------------------------------
    # Context
    # ---------------------------------------------------------

    @property
    def current_context(self) -> BrowserContext:
        self._require_open()
        return self._context # type: ignore

    @property
    def current_page(self) -> Page:
        """Kept for backward compatibility; prefer get_page(tab_id)."""
        return self.get_page(None)

    def _require_open(self) -> None:
        if not self._browser:
            raise RuntimeError("Browser is not launched. Call launch() first.")