from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource


class AnalyticsParams(ToQueryString):
    end: str = None
    label: str = None
    start: str = None
    subaccounts: str = None

    def __init__(self, end: str = None, label: str = None, start: str = None, subaccounts: str = None):
        self.end = end
        self.label = label
        self.start = start
        self.subaccounts = subaccounts

    def __iter__(self):
        yield 'end', self.end
        yield 'label', self.label
        yield 'start', self.start
        yield 'subaccounts', self.subaccounts


class AnalyticsResource(Resource):
    def by_country(self, params: AnalyticsParams = None) -> list:
        return self.__get('country', params)

    def by_date(self, params: AnalyticsParams = None) -> list:
        return self.__get('date', params)

    def by_label(self, params: AnalyticsParams = None) -> list:
        return self.__get('label', params)

    def by_subaccount(self, params: AnalyticsParams = None) -> list:
        return self.__get('subaccount', params)

    def __get(self, group_by: str, params: AnalyticsParams = None) -> list:
        if params is None:
            params = {}
        return self._client.get(f'{Endpoint.ANALYTICS.value}?group_by={group_by}&{params.as_qs()}')
