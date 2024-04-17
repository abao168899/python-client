from enum import Enum

import httpx


class OrderDirection(str, Enum):
    Ascending = "asc"
    Descending = "desc"


class SevenApi:
    apiKey: str
    baseUrl: str
    sentWith: str

    def __init__(self, api_key: str, sent_with: str = 'Python', base_url: str = 'https://gateway.seven.io/api'):
        self.apiKey = api_key
        self.baseUrl = base_url
        self.sentWith = sent_with
        self.headers = {
            'Accept': 'application/json',
            'SentWith': self.sentWith,
            'X-Api-Key': self.apiKey
        }

    def client(self):
        return httpx.Client(base_url=self.baseUrl, headers=self.headers, http2=True)