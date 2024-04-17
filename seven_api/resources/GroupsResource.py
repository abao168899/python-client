from dataclasses import dataclass
from typing import List

import marshmallow_dataclass

from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource

@dataclass
class PagingMetadata:
    count: int
    has_more: bool
    limit: int
    offset: int
    total: int

@dataclass
class Group:
    created: str
    id: int
    members_count: int
    name: str
group_schema = marshmallow_dataclass.class_schema(Group)()

@dataclass
class GroupsListResponse:
    data: List[Group]
    pagingMetadata: PagingMetadata


list_schema = marshmallow_dataclass.class_schema(GroupsListResponse)()

@dataclass
class GroupsDeleteResponse:
    success: bool


delete_schema = marshmallow_dataclass.class_schema(GroupsDeleteResponse)()


class GroupsListParams(ToQueryString):
    def __init__(self, limit: int = None, offset: int = None):
        self.limit = limit
        self.offset = offset

    def __iter__(self):
        yield 'limit', self.limit
        yield 'offset', self.offset


class GroupsResource(Resource):
    def create(self, name: str) -> Group:
        payload = {'name': name}
        with self._api.client() as client:
            return group_schema.loads(client.post(Endpoint.GROUPS.value, data=payload).text)

    def delete(self, group_id: int, delete_contacts: bool = False) -> GroupsDeleteResponse:
        params = {}
        if delete_contacts:
            params.update({'delete_contacts': 'true'})
        with self._api.client() as client:
            return delete_schema.loads(client.delete(f'{Endpoint.GROUPS.value}/{group_id}', params=params).text)

    def get(self, group_id: int) -> Group:
        with self._api.client() as client:
            return group_schema.loads(client.get(f'{Endpoint.GROUPS.value}/{group_id}').text)

    def list(self, params: GroupsListParams = None) -> GroupsListResponse:
        if params is None:
            params = GroupsListParams()
        with self._api.client() as client:
            return list_schema.loads(client.get(Endpoint.GROUPS.value, params=params.as_dict()).text)

    def update(self, group_id: int, name: str) -> Group:
        payload = {'name': name}
        with self._api.client() as client:
            return group_schema.loads(client.patch(f'{Endpoint.GROUPS.value}/{group_id}', data=payload).text)
