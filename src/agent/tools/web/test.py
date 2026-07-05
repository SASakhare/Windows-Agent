# from ddgs import DDGS
# with DDGS() as ddgs:
#     results = ddgs.text("power bank 20000mah", max_results=5)
#     for r in results:
#         print(r)

# from ddgs import DDGS
# with DDGS() as ddgs:
#     print([m for m in dir(ddgs) if not m.startswith("_")])

from duckduckgo_search import DDGS
with DDGS() as ddgs:
    print(ddgs.maps("coffee shops in Nagpur", max_results=3)) # type: ignore