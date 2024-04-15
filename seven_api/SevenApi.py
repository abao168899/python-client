from enum import Enum
from json import JSONDecodeError

import requests

from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.Method import Method

class OrderDirection(str, Enum):
    Ascending = "asc"
    Descending = "desc"


class SevenApi:
    apiKey: str
    baseUrl = 'https://gateway.seven.io/api'
    sentWith: str

    def __init__(self, api_key: str, sent_with: str = 'Python'):
        self.apiKey = api_key
        self.sentWith = sent_with
        self.headers = {
            'Accept': 'application/json',
            'SentWith': self.sentWith,
            'X-Api-Key': self.apiKey
        }
        self.kwargs = {'headers': self.headers}

    def delete(self, endpoint: Endpoint | str, params=None):
        return self.request(Method.DELETE, endpoint, params)

    def get(self, endpoint: Endpoint | str, params=None):
        return self.request(Method.GET, endpoint, params)

    def patch(self, endpoint: Endpoint | str, params=None):
        return self.request(Method.PATCH, endpoint, params)

    def post(self, endpoint: Endpoint | str, params=None):
        return self.request(Method.POST, endpoint, params)

    def request(self, method: Method, endpoint: Endpoint | str, params=None):
        if params is None:
            params = {}

        method = method.value
        if not isinstance(endpoint, str):
            endpoint = endpoint.value

        for key in list(params):
            if isinstance(params[key], bool):
                if params[key]:
                    params[key] = 1
                else:
                    params.pop(key)

        if method is Method.GET:
            self.kwargs['params'] = params
        else:
            self.kwargs['data'] = params
        url = '{}/{}'.format(self.baseUrl, endpoint)
        res = requests.request(method, url, **self.kwargs)

        try:
            json = res.json()
        except requests.exceptions.JSONDecodeError:
            json = res.text

        if res.status_code != 200:
            raise ValueError('{} {} -> {}'.format(method, url, json))
        # if res.status_code != 200 or not isinstance(json, dict) or not isinstance(json, list):
        #     raise ValueError('{} {} -> {}'.format(method, url, json))

        return json
