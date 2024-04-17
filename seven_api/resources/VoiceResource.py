from dataclasses import dataclass

import marshmallow_dataclass
from typing import List, Optional
from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource

@dataclass
class ValidateForVoiceResponse:
    error: Optional[str]
    formatted_output: Optional[str]
    id: Optional[int]
    sender: Optional[str]
    success: bool
    voice: Optional[bool]


validate_schema = marshmallow_dataclass.class_schema(ValidateForVoiceResponse)()

@dataclass
class VoiceMessage:
    error: Optional[str]
    error_text: Optional[str]
    id: Optional[int]
    price: float
    recipient: str
    sender: str
    success: bool
    text: str

@dataclass
class VoiceResponse:
    success: str
    total_price: float
    balance: float
    debug: bool
    messages: List[VoiceMessage]
dispatch_schema = marshmallow_dataclass.class_schema(VoiceResponse)()


class VoiceResource(Resource):
    def dispatch(self, to: list | str, text: str, params: dict = None) -> VoiceResponse:
        if params is None:
            params = {}

        params['text'] = text

        if isinstance(to, list):
            to = ','.join(to)
        params['to'] = to

        with self._api.client() as client:
            return dispatch_schema.loads(client.post(Endpoint.VOICE.value, data=params).text)

    def validate_phone_number(self, number: str, callback: str = None) -> ValidateForVoiceResponse:
        payload = {
            'callback': callback,
            'number': number,
        }
        with self._api.client() as client:
            return validate_schema.loads(client.post(Endpoint.VALIDATE_FOR_VOICE.value, data=payload).text)
