from dataclasses import dataclass
from typing import List, Optional

import marshmallow_dataclass

from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


@dataclass
class CountryNetwork:
    comment: Optional[str]
    features: List[str]
    mcc: str
    mncs: Optional[List[str]]
    networkName: Optional[str]
    price: float


@dataclass
class CountryPricing:
    countryCode: str
    countryName: str
    countryPrefix: str
    networks: List[CountryNetwork]


@dataclass
class PricingResponse:
    countCountries: int
    countNetworks: int
    countries: List[CountryPricing]


schema = marshmallow_dataclass.class_schema(PricingResponse)()


class PricingResource(Resource):
    def get(self, country_code: str = "") -> PricingResponse:
        params = {}
        if len(country_code) > 0:
            params.update({'country': country_code})

        with self._api.client() as client:
            return schema.loads(client.get(Endpoint.PRICING.value, params=params).text)
