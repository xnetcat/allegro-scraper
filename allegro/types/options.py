from typing import Optional, TypedDict


class Options(TypedDict):
    max_results: Optional[int]
    pages_to_fetch: Optional[int]
    start_page: Optional[int]
    use_free_proxies: Optional[bool]
    proxies_file: Optional[str]
    check_proxies: Optional[bool]
    request_timeout: Optional[int]
