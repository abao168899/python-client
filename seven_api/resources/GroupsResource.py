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

    def delete(self, group_id: int, delete_contacts: bool = False) -> dict:
        path = f'{Endpoint.GROUPS.value}/{group_id}'
        if delete_contacts:
            path += f'?delete_contacts={str(delete_contacts).lower()}'
        return self._client.delete(path)

    def get(self, group_id: int) -> dict:
        return self._client.get(f'{Endpoint.GROUPS.value}/{group_id}')

    def list(self, params: GroupsListParams) -> dict:
        return self._client.get(Endpoint.GROUPS, params.as_dict())

    def update(self, group_id: int, name: str) -> dict:
        return self._client.patch(f'{Endpoint.GROUPS.value}/{group_id}', {'name': name})
