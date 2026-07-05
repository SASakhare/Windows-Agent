# tools/search/search_tool.py
from typing import Any, Dict, List, Optional
from ddgs import DDGS

from src.agent.tools.base_tool import BaseTool


class SearchTool(BaseTool):
    """Search the web using DuckDuckGo (free, no API key required).

    Provides general web search, news, images, videos, shopping-style
    product search, and map/place lookups.
    """

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return "search"

    @property
    def description(self) -> str:
        return "Search the web: general results, news, images, videos, shopping, and places."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "web_search": self.web_search,
            "news": self.news,
            "images": self.images,
            "videos": self.videos,
            "shopping": self.shopping,
            "maps": self.maps,
        }
        if action not in actions:
            raise ValueError(f"Unknown action: {action}")
        return actions[action](**kwargs)

    # ==========================================================
    # General web search
    # ==========================================================

    def web_search(self, query: str, max_results: int = 5, region: str = "wt-wt") -> List[Dict[str, Any]]:
        """Search the general web for a query.

        Args:
            query: Search query.
            max_results: Maximum number of results to return.
            region: Region code, e.g. "us-en", "in-en", "wt-wt" (worldwide).

        Returns:
            List of dictionaries, each with title, href (url), and body (snippet).
        """
        with DDGS() as ddgs:
            results = ddgs.text(query, region=region, max_results=max_results)
        return [{"title": r.get("title"), "url": r.get("href"), "snippet": r.get("body")} for r in results]

    # ==========================================================
    # News
    # ==========================================================

    def news(self, query: str, max_results: int = 5, region: str = "wt-wt") -> List[Dict[str, Any]]:
        """Search recent news articles.

        Args:
            query: Search query.
            max_results: Maximum number of results to return.
            region: Region code, e.g. "us-en", "in-en".

        Returns:
            List of dictionaries with title, url, source, date, and snippet.
        """
        with DDGS() as ddgs:
            results = ddgs.news(query, region=region, max_results=max_results)
        return [
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "source": r.get("source"),
                "date": r.get("date"),
                "snippet": r.get("body"),
            }
            for r in results
        ]

    # ==========================================================
    # Images
    # ==========================================================

    def images(self, query: str, max_results: int = 10, region: str = "wt-wt") -> List[Dict[str, Any]]:
        """Search for images.

        Args:
            query: Search query.
            max_results: Maximum number of results to return.
            region: Region code.

        Returns:
            List of dictionaries with title, image_url, thumbnail, source_url, width, height.
        """
        with DDGS() as ddgs:
            results = ddgs.images(query, region=region, max_results=max_results)
        return [
            {
                "title": r.get("title"),
                "image_url": r.get("image"),
                "thumbnail": r.get("thumbnail"),
                "source_url": r.get("url"),
                "width": r.get("width"),
                "height": r.get("height"),
            }
            for r in results
        ]

    # ==========================================================
    # Videos
    # ==========================================================

    def videos(self, query: str, max_results: int = 10, region: str = "wt-wt") -> List[Dict[str, Any]]:
        """Search for videos.

        Args:
            query: Search query.
            max_results: Maximum number of results to return.
            region: Region code.

        Returns:
            List of dictionaries with title, url, duration, publisher, and description.
        """
        with DDGS() as ddgs:
            results = ddgs.videos(query, region=region, max_results=max_results)
        return [
            {
                "title": r.get("title"),
                "url": r.get("content"),
                "duration": r.get("duration"),
                "publisher": r.get("publisher"),
                "description": r.get("description"),
            }
            for r in results
        ]

    # ==========================================================
    # Shopping (best-effort — DDG has no dedicated shopping API)
    # ==========================================================

    def shopping(self, query: str, max_results: int = 10, region: str = "wt-wt") -> List[Dict[str, Any]]:
        """Search for products/shopping results.

        Note: DuckDuckGo has no dedicated shopping/product API, unlike
        Google Shopping. This runs a general web search biased toward
        shopping intent (adds "buy price" to the query) and returns
        text results. For real product data (price, availability,
        reviews), use BrowserTool to visit a specific retailer
        (Amazon, Flipkart) and read the page directly instead.

        Args:
            query: Product search query.
            max_results: Maximum number of results to return.
            region: Region code.

        Returns:
            List of dictionaries with title, url, and snippet.
        """
        biased_query = f"{query} buy price"
        return self.web_search(biased_query, max_results=max_results, region=region)

    # ==========================================================
    # Maps / places
    # ==========================================================

    def maps(self, query: str, place: Optional[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for places/locations.

        Note: Uses the deprecated `duckduckgo_search` package (not the
        maintained `ddgs`) since maps() was dropped in the rewrite. This
        is more likely to break silently if DuckDuckGo changes its
        backend, since duckduckgo_search no longer receives active fixes.
        If this starts failing, fall back to BrowserTool for place lookups.

        Args:
            query: What to search for, e.g. "coffee shops".
            place: Optional location context, e.g. "Nagpur, India".
            max_results: Maximum number of results to return.

        Returns:
            List of dictionaries with title, address, latitude, longitude, phone, url.
        """
        from duckduckgo_search import DDGS as LegacyDDGS  # deprecated pkg, maps() only

        full_query = f"{query} in {place}" if place else query

        try:
            with LegacyDDGS() as ddgs_1:
                results = ddgs_1.maps(full_query, max_results=max_results) # type: ignore
        except Exception as exc:
            raise RuntimeError(
                f"Maps search failed (duckduckgo_search backend may have broken): {exc}. "
                "Consider using BrowserTool to look up places directly instead."
            ) from exc

        return [
            {
                "title": r.get("title"),
                "address": r.get("address"),
                "latitude": r.get("latitude"),
                "longitude": r.get("longitude"),
                "phone": r.get("phone"),
                "url": r.get("url"),
            }
            for r in results
        ]


if __name__ == "__main__":
    tool = SearchTool()
    print(tool.execute("web_search", query="latest iPhone price"))
    print(tool.execute("news", query="ISRO launch", max_results=3))
    print(tool.execute("maps", query="coffee shops", place="Nagpur, India"))