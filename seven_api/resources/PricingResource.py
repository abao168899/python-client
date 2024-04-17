from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class PricingResource(Resource):
    def get(self, country_code: str = "") -> dict:
        path = f'{Endpoint.PRICING.value}'
        if len(country_code) > 0:
            path = f'{path}?country={country_code}'
        with self._client.client() as client:
            return client.get(path).json()
