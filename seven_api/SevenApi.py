import hashlib
import hmac
import random
import string
import time
from enum import Enum

import httpx
from httpx import Request


class OrderDirection(str, Enum):
    Ascending = "asc"
    Descending = "desc"


class SevenApi:
    def __init__(self, api_key: str, signing_secret: str = None, sent_with: str = 'Python',
                 base_url: str = 'https://gateway.seven.io/api'):
        self.apiKey = api_key
        self.baseUrl = base_url
        self.sentWith = sent_with
        self.signingSecret = signing_secret
        self.headers = {
            'Accept': 'application/json',
            'SentWith': self.sentWith,
            'X-Api-Key': self.apiKey
        }

    def sign(self, request: Request):
        if self.signingSecret is None:
            return
        timestamp = str(int(time.time()))
        nonce = str(''.join(random.choices(string.ascii_letters + string.digits, k=32)))
        md5 = hashlib.md5(request.read()).hexdigest()
        to_sign = '\n'.join([timestamp, nonce, request.method.upper(), str(request.url), md5]).encode()
        signature = hmac.new(self.signingSecret.encode(), to_sign, hashlib.sha256).hexdigest()

        request.headers.update({
            'X-Nonce': nonce,
            'X-Signature': signature,
            'X-Timestamp': timestamp
        })

    def pre_request(self, request: Request):
        self.sign(request)

    def client(self):
        event_hooks = {'request': [self.pre_request]}
        return httpx.Client(base_url=self.baseUrl, event_hooks=event_hooks, headers=self.headers, http2=True)
