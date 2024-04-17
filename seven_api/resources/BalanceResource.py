from dataclasses import dataclass

import marshmallow_dataclass

from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


@dataclass
class Balance:
    amount: float
    currency: str


schema = marshmallow_dataclass.class_schema(Balance)()


class BalanceResource(Resource):
    def retrieve(self) -> Balance:
        with self._api.client() as client:
            return schema.loads(client.get(Endpoint.BALANCE.value).text)
