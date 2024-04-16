from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class SubaccountsResource(Resource):
    def auto_charge(self, subaccount_id: int, amount: float, threshold: float) -> dict:
        params = {
            'action': 'update',
            'amount': amount,
            'id': subaccount_id,
            'threshold': threshold
        }
        return self._client.post(Endpoint.SUBACCOUNTS, params)

    def create(self, email: str, name: str) -> dict:
        params = {
            'action': 'create',
            'email': email,
            'name': name,
        }
        return self._client.post(Endpoint.SUBACCOUNTS, params)

    def delete(self, subaccount_id: int) -> dict:
        params = {
            'action': 'delete',
            'id': subaccount_id,
        }
        return self._client.post(Endpoint.SUBACCOUNTS, params)

    def list(self, subaccount_id: int = None) -> list:
        path = f'{Endpoint.SUBACCOUNTS.value}?action=read'
        if subaccount_id is not None:
            path += f'&id={subaccount_id}'
        return self._client.get(path)

    def transfer_credits(self, subaccount_id: int, amount: float) -> dict:
        params = {
            'action': 'transfer_credits',
            'amount': amount,
            'id': subaccount_id,
        }
        return self._client.post(Endpoint.SUBACCOUNTS, params)
