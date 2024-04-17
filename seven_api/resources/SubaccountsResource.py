from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class SubaccountsResource(Resource):
    def auto_charge(self, subaccount_id: int, amount: float, threshold: float) -> dict:
        payload = {
            'action': 'update',
            'amount': amount,
            'id': subaccount_id,
            'threshold': threshold
        }
        with self.__api.client() as client:
            return client.post(Endpoint.SUBACCOUNTS.value, data=payload).json()

    def create(self, email: str, name: str) -> dict:
        payload = {
            'action': 'create',
            'email': email,
            'name': name,
        }
        with self.__api.client() as client:
            return client.post(Endpoint.SUBACCOUNTS.value, data=payload).json()

    def delete(self, subaccount_id: int) -> dict:
        payload = {
            'action': 'delete',
            'id': subaccount_id,
        }
        with self.__api.client() as client:
            return client.post(Endpoint.SUBACCOUNTS.value, data=payload).json()

    def list(self, subaccount_id: int = None) -> list:
        params = {'action': 'read'}
        if subaccount_id is not None:
            params.update({'id': subaccount_id})
        with self.__api.client() as client:
            return client.get(Endpoint.SUBACCOUNTS.value, params=params).json()

    def transfer_credits(self, subaccount_id: int, amount: float) -> dict:
        payload = {
            'action': 'transfer_credits',
            'amount': amount,
            'id': subaccount_id,
        }
        with self.__api.client() as client:
            return client.post(Endpoint.SUBACCOUNTS.value, data=payload).json()
