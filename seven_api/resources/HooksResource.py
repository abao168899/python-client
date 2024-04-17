from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ExtendedEnum import ExtendedEnum
from seven_api.resources.Resource import Resource


class HooksResource(Resource):
    def read(self) -> dict:
        with self._client.client() as client:
            return client.get(Endpoint.HOOKS.value).json()

    def subscribe(self, params: dict) -> dict:
        with self._client.client() as client:
            return client.post(Endpoint.HOOKS.value, data=params).json()

    def unsubscribe(self, hook_id: int) -> dict:
        with self._client.client() as client:
            return client.delete(f'{Endpoint.HOOKS.value}?id={hook_id}').json()


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
