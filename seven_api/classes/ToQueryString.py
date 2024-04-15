from abc import abstractmethod
from urllib.parse import urlencode

class ToQueryString:
    @abstractmethod
    def __iter__(self):
       pass

    def as_dict(self) -> dict:
        return {k: v for k, v in dict(self).items() if v is not None}

    def as_qs(self) -> str:
        return urlencode(self.as_dict())