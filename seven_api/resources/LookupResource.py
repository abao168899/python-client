from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


class LookupResource(Resource):
    def cnam(self, number: str) -> list:
        return self.__post('cnam', number)

    def hlr(self, params=None) -> list:
        return self.__post('hlr', params)

    def mnp(self, params=None) -> list:
        return self.__post('mnp', params)

    def format(self, params=None) -> list:
        return self.__post('format', params)

    def rcs(self, params=None) -> list:
        return self.__post('rcs', params)

    def __post(self, lookup_type: str, number: str) -> list:
        res = self._client.get('{}/{}?number={}'.format(Endpoint.LOOKUP.value, lookup_type, number))
        
        if isinstance(res, dict):
            return [res]
        return res

