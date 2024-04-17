from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class LookupResource(Resource):
    def cnam(self, numbers: str | list) -> list:
        return self.__get('cnam', numbers)

    def hlr(self, numbers: str | list) -> list:
        return self.__get('hlr', numbers)

    def mnp(self, numbers: str | list) -> list:
        return self.__get('mnp', numbers)

    def format(self, numbers: str | list) -> list:
        return self.__get('format', numbers)

    def rcs(self, numbers: str | list) -> list:
        return self.__get('rcs', numbers)

    def __get(self, lookup_type: str, numbers: str | list) -> list:
        if isinstance(numbers, list):
            numbers = ','.join(numbers)

        with self.__api.client() as client:
            res = client.get(f'{Endpoint.LOOKUP.value}/{lookup_type}', params={'number': numbers}).json()
            return [res] if isinstance(res, dict) else res
