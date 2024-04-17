from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class BalanceResource(Resource):
    def retrieve(self) -> dict:
        with self.__api.client as client:
            return client.get(Endpoint.BALANCE.value).json()