from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class VoiceResource(Resource):
    def dispatch(self, to: list | str, text: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        params['text'] = text

        if isinstance(to, list):
            to = ','.join(to)
        params['to'] = to

        with self.__api.client() as client:
            return client.post(Endpoint.VOICE.value, data=params).json()

    def validate_phone_number(self, number: str, callback: str = None) -> dict:
        payload = {
            'callback': callback,
            'number': number,
        }
        with self.__api.client() as client:
            return client.post(Endpoint.VALIDATE_FOR_VOICE.value, data=payload).json()
