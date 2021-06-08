from typing import Optional, TypedDict


class Options(TypedDict):
    sponsored_offers: Optional[bool]
    max_results: Optional[int]
    pages_to_fetch: Optional[int]
    start_page: Optional[int]
