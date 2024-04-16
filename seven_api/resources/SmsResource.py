from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ExtendedEnum import ExtendedEnum
from seven_api.resources.Resource import Resource


class SmsResource(Resource):
    def delete(self, ids: list | str) -> dict:
        if isinstance(ids, str):
            ids = [ids]
        ids = ','.join(ids)
        return self._client.delete(f'{Endpoint.SMS.value}?ids[]={ids}')

    def dispatch(self, to: list | str, text: str, params: dict = None) -> dict:
        if params is None:
            params = {}
        params['text'] = text
        if isinstance(to, list):
            to = ','.join(to)
        params['to'] = to
        return self._client.post(Endpoint.SMS, params)

    def status(self, ids: list | str) -> list:
        if isinstance(ids, str):
            ids = [ids]
        ids = ','.join(ids)
        return self._client.get(f'{Endpoint.STATUS.value}?msg_id={ids}')


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
