from dataclasses import dataclass
from typing import Optional, List

import marshmallow_dataclass
from marshmallow import EXCLUDE

from seven_api.SevenApi import OrderDirection
from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource, PagingMetadata
from urllib.parse import urlencode


@dataclass
class ContactValidation:
    state: Optional[str]
    timestamp: Optional[str]


@dataclass
class ContactInitials:
    color: str
    initials: str


@dataclass
class ContactProperties:
    firstname: Optional[str]
    fullname: Optional[str]
    lastname: Optional[str]
    mobile_number: Optional[str]
    home_number: Optional[str]
    email: Optional[str]
    address: Optional[str]
    postal_code: Optional[str]
    city: Optional[str]
    birthday: Optional[str]
    notes: Optional[str]
    class Meta:
        unknown = EXCLUDE


@dataclass
class Contact:
    avatar: Optional[str]
    created: str
    groups: List[int]
    id: int
    initials: ContactInitials
    properties: ContactProperties
    validation: ContactValidation


contact_schema = marshmallow_dataclass.class_schema(Contact)()


@dataclass
class ContactsListResponse:
    data: List[Contact]
    pagingMetadata: PagingMetadata


list_schema = marshmallow_dataclass.class_schema(ContactsListResponse)()


class ContactsListParams:
    def __init__(self, group_id: int = None, limit: int = None, offset: int = None, order_by: str = None,
                 order_direction: OrderDirection = OrderDirection.Ascending, search: str = None):
        self.group_id = group_id
        self.limit = limit
        self.offset = offset
        self.order_by = order_by
        self.order_direction = order_direction
        self.search = search

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
    def create(self, properties: dict, avatar: str = None, groups: list = None) -> Contact:
        if groups is None:
            groups = []

        if avatar is not None:
            properties['avatar'] = avatar
        if groups is not None:
            properties['groups'] = groups

        with self._api.client() as client:
            return contact_schema.loads(client.post(Endpoint.CONTACTS.value, data=properties).text)

    def delete(self, contact_id: int):
        with self._api.client() as client:
            client.delete(f'{Endpoint.CONTACTS.value}/{contact_id}')

    def get(self, contact_id: int) -> Contact:
        with self._api.client() as client:
            return contact_schema.loads(client.get(f'{Endpoint.CONTACTS.value}/{contact_id}').text)

    def list(self, params: ContactsListParams = None) -> ContactsListResponse:
        if params is None:
            params = ContactsListParams()
        with self._api.client() as client:
            return list_schema.loads(client.get(Endpoint.CONTACTS.value, params=params.as_dict()).text)

    def update(self, params: dict) -> Contact:
        contact_id = params['id']
        del params['id']

        with self._api.client() as client:
            return contact_schema.loads(client.patch(f'{Endpoint.CONTACTS.value}/{contact_id}', data=params).text)
