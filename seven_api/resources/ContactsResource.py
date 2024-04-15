from seven_api.SevenApi import OrderDirection
from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource
from urllib.parse import urlencode


class ContactsListParams:
    group_id: int = None
    limit: int = None
    offset: int = None
    order_by: str = None
    order_direction: OrderDirection = OrderDirection.Ascending
    search: str = None

    def __iter__(self):
        yield 'group_id', self.group_id
        yield 'limit', self.limit
        yield 'offset', self.offset
        yield 'order_by', self.order_by
        yield 'order_direction', self.order_direction.value
        yield 'search', self.search

    def as_dict(self) -> dict:
        return {k: v for k, v in dict(self).items() if v is not None}

    def as_qs(self) -> str:
        return urlencode(self.as_dict())


class ContactsResource(Resource):
    def create(self, properties: dict, avatar=None, groups=None) -> dict:
        if groups is None:
            groups = []

        properties['avatar'] = avatar
        properties['groups'] = groups

        return self._client.post(Endpoint.CONTACTS, properties)

    def delete(self, contact_id: int):
        self._client.delete(f'{Endpoint.CONTACTS.value}/{contact_id}')

    def get(self, contact_id: int) -> dict:
        return self._client.get(f'{Endpoint.CONTACTS.value}/{contact_id}')

    def list(self, params: ContactsListParams) -> dict:
        return self._client.get(f'{Endpoint.CONTACTS.value}?{params.as_qs()}')

    def update(self, params: dict) -> dict:
        contact_id = params['id']
        del params['id']
        return self._client.patch(f'{Endpoint.CONTACTS.value}/{contact_id}', params)
