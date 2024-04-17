from dataclasses import dataclass
from typing import Optional, List

import marshmallow_dataclass

from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource

@dataclass
class SubaccountAutoTopUp:
    amount: Optional[float]
    threshold: Optional[float]

@dataclass
class SubaccountContact:
    email: str
    name: str


@dataclass
class Subaccount:
    auto_topup: SubaccountAutoTopUp
    balance: float
    company: str
    contact: SubaccountContact
    id: int
    total_usage: float
    username: Optional[str]

subaccount_schema = marshmallow_dataclass.class_schema(Subaccount)()

@dataclass
class SubaccountCreateResponse:
    error: Optional[str]
    subaccount: Optional[Subaccount]
    success: bool

create_schema = marshmallow_dataclass.class_schema(SubaccountCreateResponse)()

@dataclass
class SubaccountDeleteResponse:
    error: Optional[str]
    success: bool

delete_schema = marshmallow_dataclass.class_schema(SubaccountDeleteResponse)()

@dataclass
class TransferCreditsResponse:
    error: Optional[str]
    success: bool

transfer_schema = marshmallow_dataclass.class_schema(TransferCreditsResponse)()

@dataclass
class AutoChargeResponse:
    error: Optional[str]
    success: bool

auto_charge_schema = marshmallow_dataclass.class_schema(AutoChargeResponse)()

class SubaccountsResource(Resource):
    def auto_charge(self, subaccount_id: int, amount: float, threshold: float) -> AutoChargeResponse:
        payload = {
            'action': 'update',
            'amount': amount,
            'id': subaccount_id,
            'threshold': threshold
        }
        with self._api.client() as client:
            return auto_charge_schema.loads(client.post(Endpoint.SUBACCOUNTS.value, data=payload).text)

    def create(self, email: str, name: str) -> SubaccountCreateResponse:
        payload = {
            'action': 'create',
            'email': email,
            'name': name,
        }
        with self._api.client() as client:
            return create_schema.loads(client.post(Endpoint.SUBACCOUNTS.value, data=payload).text)

    def delete(self, subaccount_id: int) -> SubaccountDeleteResponse:
        payload = {
            'action': 'delete',
            'id': subaccount_id,
        }
        with self._api.client() as client:
            return delete_schema.loads(client.post(Endpoint.SUBACCOUNTS.value, data=payload).text)

    def list(self, subaccount_id: int = None) -> List[Subaccount]:
        params = {'action': 'read'}
        if subaccount_id is not None:
            params.update({'id': subaccount_id})
        with self._api.client() as client:
            return subaccount_schema.loads(client.get(Endpoint.SUBACCOUNTS.value, params=params).text, many=True)

    def transfer_credits(self, subaccount_id: int, amount: float) -> TransferCreditsResponse:
        payload = {
            'action': 'transfer_credits',
            'amount': amount,
            'id': subaccount_id,
        }
        with self._api.client() as client:
            return transfer_schema.loads(client.post(Endpoint.SUBACCOUNTS.value, data=payload).text)
