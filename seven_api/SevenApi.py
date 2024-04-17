from enum import Enum

import requests

from seven_api.classes.Endpoint import Endpoint


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
        self.kwargs = {'headers': self.headers}
        self.req = requests.Session()
        self.req.headers = self.headers

    def delete(self, endpoint: Endpoint | str, params: dict = None):
        return self.__request('DELETE', endpoint, params)

    def get(self, endpoint: Endpoint | str, params: dict = None):
        self.req.params = params
        return self.__request('GET', endpoint, None, params)

    def patch(self, endpoint: Endpoint | str, params: dict = None):
        return self.__request('PATCH', endpoint, params)

    def post(self, endpoint: Endpoint | str, params: dict = None):
        return self.__request('POST', endpoint, params)

    def __request(self, method: str, endpoint: Endpoint | str, params: dict = None, qs: dict = None):
        if not isinstance(endpoint, str):
            endpoint = endpoint.value

        if params is None:
            params = {}

        if qs is None:
            qs = {}

        for key in list(params):
            if isinstance(params[key], bool):
                if params[key]:
                    params[key] = 1
                else:
                    params.pop(key)

        self.kwargs['data'] = params

        url = '{}/{}'.format(self.baseUrl, endpoint)
        # res = self.req.request(method, url, **self.kwargs)
        self.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        print('{} {} with data {} and headers {} and params {}'.format(method, url, params, self.headers, qs))
        res = requests.request(method, url, data=params, headers=self.headers, params=qs)

        try:
            json = res.json()
        except requests.exceptions.JSONDecodeError:
            json = res.text

        if res.status_code != 200:
            raise ValueError('{} {} -> {}'.format(method, url, json))

        return json
