from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class HooksResource(Resource):
    def read(self) -> dict:
        return self._client.get(Endpoint.HOOKS)

    def subscribe(self, params: dict) -> dict:
        return self._client.post(Endpoint.HOOKS, params)

    def unsubscribe(self, hook_id: int) -> dict:
        return self._client.delete(f'{Endpoint.HOOKS.value}?id={hook_id}')
