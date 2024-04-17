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
        with self.__api.client() as client:
            return client.post(Endpoint.GROUPS.value, data={'name': name}).json()

    def delete(self, group_id: int, delete_contacts: bool = False) -> dict:
        path = f'{Endpoint.GROUPS.value}/{group_id}'
        if delete_contacts:
            path += f'?delete_contacts={str(delete_contacts).lower()}'
        with self.__api.client() as client:
            return client.delete(path).json()

    def get(self, group_id: int) -> dict:
        with self.__api.client() as client:
            return client.get(f'{Endpoint.GROUPS.value}/{group_id}').json()

    def list(self, params: GroupsListParams) -> dict:
        with self.__api.client() as client:
            return client.get(Endpoint.GROUPS.value, params=params.as_dict()).json()

    def update(self, group_id: int, name: str) -> dict:
        with self.__api.client() as client:
            return client.patch(f'{Endpoint.GROUPS.value}/{group_id}', data={'name': name}).json()
