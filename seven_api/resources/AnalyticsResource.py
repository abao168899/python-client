from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource


class AnalyticsParams(ToQueryString):
    end: str = None
    label: str = None
    start: str = None
    subaccounts: str = None

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
            params = AnalyticsParams()
        payload = params.as_dict()
        payload['group_by'] = group_by
        with self.__api.client() as client:
            return client.get(Endpoint.ANALYTICS.value, params=payload).json()
