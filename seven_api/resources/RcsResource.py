from dataclasses import dataclass
from typing import Optional, List

import marshmallow_dataclass

from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource
from enum import Enum


@dataclass
class RcsMessage:
    channel: str
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
class RcsResponse:
    balance: float
    debug: str
    messages: List[RcsMessage]
    sms_type: str
    success: str
    total_price: float


dispatch_schema = marshmallow_dataclass.class_schema(RcsResponse)()

@dataclass
class RcsDeleteResponse:
    success: bool
delete_schema = marshmallow_dataclass.class_schema(RcsDeleteResponse)()

@dataclass
class RcsEventResponse:
    success: bool
event_schema = marshmallow_dataclass.class_schema(RcsEventResponse)()

class RcsEvent(Enum):
    IS_TYPING = 0
    READ = 1


class RcsTarget(str, Enum):
    PHONE_NUMBER = 'to'
    MESSAGE_ID = 'msg_id'


class RcsResource(Resource):
    def delete(self, msg_id: str) -> RcsDeleteResponse:
        with self._api.client() as client:
            return delete_schema.loads(client.delete(f'{Endpoint.RCS_MESSAGES.value}/{msg_id}').text)

    def dispatch(self, to: str, text: str, params: dict = None) -> RcsResponse:
        if params is None:
            params = {}
        params['to'] = to
        params['text'] = text

        with self._api.client() as client:
            return dispatch_schema.loads(client.post(Endpoint.RCS_MESSAGES.value, data=params).text)

    def event(self, target: RcsTarget, event: RcsEvent, value, agent='') -> RcsEventResponse:
        key = target.value
        params = {'event': event.name, key: value, 'from': agent}

        with self._api.client() as client:
            return event_schema.loads(client.post(Endpoint.RCS_EVENTS.value, data=params).text)
