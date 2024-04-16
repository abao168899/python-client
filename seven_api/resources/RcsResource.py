from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource
from enum import Enum


class RcsEvent(Enum):
    IS_TYPING = 0
    READ = 1


class RcsTarget(str, Enum):
    PHONE_NUMBER = 'to'
    MESSAGE_ID = 'msg_id'


class RcsResource(Resource):
    def delete(self, msg_id: int) -> dict:
        return self._client.delete(f'{Endpoint.RCS.value}/messages/{msg_id}')

    def dispatch(self, to: str, text: str, params=None) -> dict:
        if params is None:
            params = {}
        params['to'] = to
        params['text'] = text
        return self._client.post(f'{Endpoint.RCS.value}/messages', params)

    def event(self, target: RcsTarget, event: RcsEvent, value, agent='') -> dict:
        key = target.value

        params = {'event': event.name, key: value, 'from': agent}
        return self._client.post(f'{Endpoint.RCS.value}/events', params)
