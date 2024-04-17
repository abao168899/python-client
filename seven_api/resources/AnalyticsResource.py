from dataclasses import dataclass
from typing import List

import marshmallow_dataclass
from marshmallow import Schema

from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource


@dataclass
class AnalyticsBase:
    sms: int
    voice: int
    hlr: int
    mnp: int
    inbound: int
    usage_eur: float


@dataclass
class AnalyticsByCountry(AnalyticsBase):
    country: str


country_schema = marshmallow_dataclass.class_schema(AnalyticsByCountry)()


@dataclass
class AnalyticsByDate(AnalyticsBase):
    date: str


date_schema = marshmallow_dataclass.class_schema(AnalyticsByDate)()


@dataclass
class AnalyticsBySubaccount(AnalyticsBase):
    account: str


subaccount_schema = marshmallow_dataclass.class_schema(AnalyticsBySubaccount)()


@dataclass
class AnalyticsByLabel(AnalyticsBase):
    label: str


label_schema = marshmallow_dataclass.class_schema(AnalyticsByLabel)()


class AnalyticsParams(ToQueryString):
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
    def by_country(self, params: AnalyticsParams = None) -> List[AnalyticsByCountry]:
        return self.__get('country', country_schema, params)

    def by_date(self, params: AnalyticsParams = None) -> List[AnalyticsByDate]:
        return self.__get('date', date_schema, params)

    def by_label(self, params: AnalyticsParams = None) -> List[AnalyticsByLabel]:
        return self.__get('label', label_schema, params)

    def by_subaccount(self, params: AnalyticsParams = None) -> List[AnalyticsBySubaccount]:
        return self.__get('subaccount', subaccount_schema, params)

    def __get(self, group_by: str, schema: Schema, params: AnalyticsParams = None) -> list:
        if params is None:
            params = AnalyticsParams()
        payload = params.as_dict()
        payload['group_by'] = group_by
        with self._api.client() as client:
            text = client.get(Endpoint.ANALYTICS.value, params=payload).text
            return schema.loads(text, many=True)
