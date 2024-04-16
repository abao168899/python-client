from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class SubaccountsResource(Resource):
    def auto_charge(self, subaccount_id: int, amount: float, threshold: float) -> dict:
        return self._client.post(Endpoint.SUBACCOUNTS, {
            'action': 'update',
            'amount': amount,
            'id': subaccount_id,
            'threshold': threshold
        })

    def create(self, email: str, name: str) -> dict:
        return self._client.post(Endpoint.SUBACCOUNTS, {
            'action': 'create',
            'email': email,
            'name': name,
        })

    def delete(self, subaccount_id: int) -> dict:
        return self._client.post(Endpoint.SUBACCOUNTS, {
            'action': 'delete',
            'id': subaccount_id,
        })

    def list(self, subaccount_id: int = None) -> list:
        params = {'action': 'read'}
        if subaccount_id is not None:
            params.update({'id': subaccount_id})
        return self._client.get(Endpoint.SUBACCOUNTS, params)

    def transfer_credits(self, subaccount_id: int, amount: float) -> dict:
        return self._client.post(Endpoint.SUBACCOUNTS, {
            'action': 'transfer_credits',
            'amount': amount,
            'id': subaccount_id,
        })
