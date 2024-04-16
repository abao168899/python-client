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

        return self._client.post(Endpoint.VOICE, params)

    def validate_phone_number(self, number: str, callback: str = None) -> dict:
        params = {
            'callback': callback,
            'number': number,
        }
        return self._client.post(Endpoint.VALIDATE_FOR_VOICE, params)
