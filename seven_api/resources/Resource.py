from dataclasses import dataclass

from seven_api.SevenApi import SevenApi


@dataclass
class PagingMetadata:
    count: int
    has_more: bool
    limit: int
    offset: int
    total: int


class Resource:
    def __init__(self, client: SevenApi):
        self._api = client
