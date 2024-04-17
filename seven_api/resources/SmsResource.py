from dataclasses import dataclass
from typing import List, Optional

import marshmallow_dataclass

from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ExtendedEnum import ExtendedEnum
from seven_api.resources.Resource import Resource

@dataclass
class SmsMessage:
    encoding: str
    error: Optional[str]
    error_text: Optional[str]
    id: Optional[str]
    is_binary: bool
    label: Optional[str]
    parts: int
    price: float
    recipient: str
    sender: str
    success: bool
    text: str
    udh: Optional[str]


@dataclass
class SmsResponse:
    balance: float
    debug: str
    messages: List[SmsMessage]
    sms_type: str
    success: str
    total_price: float
dispatch_schema = marshmallow_dataclass.class_schema(SmsResponse)()

@dataclass
class SmsDeleteResponse:
    deleted: List[str]
    success: bool
delete_schema = marshmallow_dataclass.class_schema(SmsDeleteResponse)()

@dataclass
class SmsStatus:
    id: str
    status: Optional[str]
    status_time: Optional[str]
status_schema = marshmallow_dataclass.class_schema(SmsStatus)()

class SmsResource(Resource):
    def delete(self, ids: list | str) -> SmsDeleteResponse:
        if isinstance(ids, str):
            ids = [ids]
        ids = ','.join(ids)

        with self._api.client() as client:
            return delete_schema.loads(client.delete(Endpoint.SMS.value, params={'ids[]': ids}).text)

    def dispatch(self, to: list | str, text: str, params: dict = None) -> SmsResponse:
        if params is None:
            params = {}
        params['text'] = text
        if isinstance(to, list):
            to = ','.join(to)
        params['to'] = to

        with self._api.client() as client:
            return dispatch_schema.loads(client.post(Endpoint.SMS.value, data=params).text)

    def status(self, ids: list | str) -> List[SmsStatus]:
        if isinstance(ids, str):
            ids = [ids]
        ids = ','.join(ids)

        with self._api.client() as client:
            return status_schema.loads(client.get(Endpoint.STATUS.value, params={'msg_id': ids}).text, many=True)


class StatusMessage(ExtendedEnum):
    DELIVERED = 0
    NOTDELIVERED = 1
    BUFFERED = 2
    TRANSMITTED = 3
    ACCEPTED = 4
    EXPIRED = 5
    REJECTED = 6
    FAILED = 7
    UNKNOWN = 8
