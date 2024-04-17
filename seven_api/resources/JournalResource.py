from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource


class JournalParams(ToQueryString):
    date_from: str = None
    date_to: str = None
    id: int = None
    limit: int = None
    offset: int = None
    state: str = None
    to: str = None

    def __iter__(self):
        yield 'date_from', self.date_from
        yield 'date_to', self.date_to
        yield 'id', self.id
        yield 'limit', self.limit
        yield 'offset', self.offset
        yield 'state', self.state
        yield 'to', self.to


class JournalResource(Resource):
    def outbound(self, params: JournalParams = None) -> list:
        return self.__get('outbound', params)

    def inbound(self, params: JournalParams = None) -> list:
        return self.__get('inbound', params)

    def voice(self, params: JournalParams = None) -> list:
        return self.__get('voice', params)

    def replies(self, params: JournalParams = None) -> list:
        return self.__get('replies', params)

    def __get(self, journal_type: str, params: JournalParams = None) -> list:
        if params is None:
            params = JournalParams()

        with self._client.client() as client:
            return client.get(f'{Endpoint.JOURNAL.value}/{journal_type}', params=params.as_dict()).json()
