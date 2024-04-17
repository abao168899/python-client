from dataclasses import field, dataclass
from typing import Optional, List

import marshmallow_dataclass
from marshmallow import Schema

from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource


@dataclass
class JournalBase:
    from_: str = field(metadata={"data_key": "from"})
    id: str
    price: str
    text: str
    timestamp: str
    to: str


base_schema = marshmallow_dataclass.class_schema(JournalBase)()


@dataclass
class JournalOutbound(JournalBase):
    channel: str
    connection: str
    dlr: Optional[str]
    dlr_timestamp: Optional[str]
    foreign_id: Optional[str]
    label: Optional[str]
    latency: Optional[str]
    mccmnc: Optional[str]
    type: str


outbound_schema = marshmallow_dataclass.class_schema(JournalOutbound)()


@dataclass
class JournalVoice(JournalBase):
    duration: Optional[str]
    error: Optional[str]
    price: Optional[str]
    status: str
    xml: bool


voice_schema = marshmallow_dataclass.class_schema(JournalVoice)()


@dataclass
class JournalReply(JournalBase):
    price: float


reply_schema = marshmallow_dataclass.class_schema(JournalReply)()


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
    def outbound(self, params: JournalParams = None) -> List[JournalOutbound]:
        return self.__get(Endpoint.JOURNAL_OUTBOUND, outbound_schema, params)

    def inbound(self, params: JournalParams = None) -> List[JournalBase]:
        return self.__get(Endpoint.JOURNAL_INBOUND, base_schema, params)

    def voice(self, params: JournalParams = None) -> List[JournalVoice]:
        return self.__get(Endpoint.JOURNAL_VOICE, voice_schema, params)

    def replies(self, params: JournalParams = None) -> List[JournalReply]:
        return self.__get(Endpoint.JOURNAL_REPLIES, reply_schema, params)

    def __get(self, endpoint: Endpoint, schema: Schema, params: JournalParams = None) -> list:
        if params is None:
            params = JournalParams()

        with self._api.client() as client:
            return schema.loads(client.get(endpoint.value, params=params.as_dict()).text, many=True)
