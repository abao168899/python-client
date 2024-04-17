from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ExtendedEnum import ExtendedEnum
from seven_api.resources.Resource import Resource


class SmsResource(Resource):
    def delete(self, ids: list | str) -> dict:
        if isinstance(ids, str):
            ids = [ids]
        ids = ','.join(ids)

        with self.__api.client() as client:
            return client.delete(Endpoint.SMS.value, params={'ids[]': ids}).json()

    def dispatch(self, to: list | str, text: str, params: dict = None) -> dict:
        if params is None:
            params = {}
        params['text'] = text
        if isinstance(to, list):
            to = ','.join(to)
        params['to'] = to

        with self.__api.client() as client:
            return client.post(Endpoint.SMS.value, data=params).json()

    def status(self, ids: list | str) -> list:
        if isinstance(ids, str):
            ids = [ids]
        ids = ','.join(ids)

        with self.__api.client() as client:
            return client.get(Endpoint.STATUS.value, params={'msg_id': ids}).json()


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
