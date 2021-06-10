from typing import Optional, TypedDict


class Options(TypedDict):
    include_sponsored_offers: Optional[bool]
    max_results: Optional[int]
    pages_to_fetch: Optional[int]
    start_page: Optional[int]
    avoid_duplicates: Optional[bool]
    use_free_proxies: Optional[bool]
    proxies_file: Optional[str]
    check_proxies: Optional[bool]
    request_timeout: Optional[int]
