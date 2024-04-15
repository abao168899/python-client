from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource


class GroupsListParams(ToQueryString):
    limit: int = None
    offset: int = None

    def __iter__(self):
        yield 'limit', self.limit
        yield 'offset', self.offset


class GroupsResource(Resource):
    def create(self, name: str) -> dict:
        return self._client.post(Endpoint.GROUPS, {'name': name})

    def delete(self, group_id: int) -> dict:
        return self._client.delete(f'{Endpoint.GROUPS.value}/{group_id}')

    def get(self, group_id: int) -> dict:
        return self._client.get(f'{Endpoint.GROUPS.value}/{group_id}')

    def list(self, params: GroupsListParams) -> dict:
        return self._client.get(f'{Endpoint.GROUPS.value}?{params.as_qs()}')

    def update(self, group_id: int, name: str) -> dict:
        return self._client.patch(f'{Endpoint.GROUPS.value}/{group_id}', {'name': name})
