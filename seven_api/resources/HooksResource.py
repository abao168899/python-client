from dataclasses import dataclass
from typing import Optional, List

import marshmallow_dataclass
from marshmallow import EXCLUDE

from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ExtendedEnum import ExtendedEnum
from seven_api.resources.Resource import Resource

@dataclass
class Hook:
    created: str
    enabled: bool
    event_filter: Optional[str]
    event_type: str
    id: str
    request_method: str
    target_url: str

@dataclass
class HooksReadResponse:
    hooks: List[Hook]
    success: bool


read_schema = marshmallow_dataclass.class_schema(HooksReadResponse)()

@dataclass
class HooksSubscribeResponse:
    error_message: Optional[str]
    id: Optional[int]
    success: bool


subscribe_schema = marshmallow_dataclass.class_schema(HooksSubscribeResponse)()

@dataclass
class HooksUnsubscribeResponse:
    error_message: Optional[str]
    id: Optional[int]
    success: bool


unsubscribe_schema = marshmallow_dataclass.class_schema(HooksUnsubscribeResponse)()

class HooksResource(Resource):
    def read(self) -> HooksReadResponse:
        with self._api.client() as client:
            return read_schema.loads(client.get(Endpoint.HOOKS.value).text, unknown=EXCLUDE)

    def subscribe(self, params: dict) -> HooksSubscribeResponse:
        with self._api.client() as client:
            return subscribe_schema.loads(client.post(Endpoint.HOOKS.value, data=params).text, unknown=EXCLUDE)

    def unsubscribe(self, hook_id: int) -> HooksUnsubscribeResponse:
        params = {'id': hook_id}
        with self._api.client() as client:
            return unsubscribe_schema.loads(client.delete(Endpoint.HOOKS.value, params=params).text, unknown=EXCLUDE)


class HookEventType(ExtendedEnum):
    ALL = 'all'
    SMS_STATUS = 'dlr'
    SMS_INBOUND = 'sms_mo'
    TRACKING = 'tracking'
    VOICE_CALL = 'voice_call'
    VOICE_STATUS = 'voice_status'


class HookRequestMethod(ExtendedEnum):
    GET = 'GET'
    JSON = 'JSON'
    POST = 'POST'
