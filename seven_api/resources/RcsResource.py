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
        with self.__api.client() as client:
            return client.delete(f'{Endpoint.RCS_MESSAGES.value}/{msg_id}').json()

    def dispatch(self, to: str, text: str, params=None) -> dict:
        if params is None:
            params = {}
        params['to'] = to
        params['text'] = text

        with self.__api.client() as client:
            return client.post(Endpoint.RCS_MESSAGES.value, data=params).json()

    def event(self, target: RcsTarget, event: RcsEvent, value, agent='') -> dict:
        key = target.value
        params = {'event': event.name, key: value, 'from': agent}

        with self.__api.client() as client:
            return client.post(Endpoint.RCS_EVENTS.value, data=params).json()
