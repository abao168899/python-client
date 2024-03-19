import requests

from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.Method import Method


class SevenApi:
    apiKey: str
    baseUrl = 'https://gateway.seven.io/api'
    sentWith: str

    def __init__(self, api_key: str, sent_with: str = 'Python'):
        self.apiKey = api_key
        self.sentWith = sent_with

    def delete(self, endpoint: Endpoint | str, params=None):
        return self.request(Method.DELETE, endpoint, params)

    def get(self, endpoint: Endpoint | str, params=None):
        return self.request(Method.GET, endpoint, params)

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

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'SentWith': self.sentWith,
            'X-Api-Key': self.apiKey
        }
        kwargs = {'headers': headers}
        if method is Method.GET:
            kwargs['params'] = params
        else:
            kwargs['json'] = params
        url = '{}/{}'.format(self.baseUrl, endpoint)
        res = requests.request(method, url, **kwargs)
        json = res.json()

        # if res.status_code != 200 or not isinstance(json, dict) or not isinstance(json, list):
        #     raise ValueError('{} {} -> {}'.format(method, url, json))

        if res.status_code != 200:
            raise ValueError('{} {} -> {}'.format(method, url, json))

        return json
