from dataclasses import dataclass
from typing import List, Optional

import marshmallow_dataclass
from marshmallow import Schema

from seven_api.classes.Endpoint import Endpoint
from seven_api.resources.Resource import Resource


@dataclass
class CnamLookup:
    code: str
    name: str
    number: str
    success: str


cnam_schema = marshmallow_dataclass.class_schema(CnamLookup)()


@dataclass
class Carrier:
    network_code: str
    name: str
    country: str
    network_type: str


@dataclass
class HlrLookup:
    status: bool
    status_message: str
    lookup_outcome: bool
    lookup_outcome_message: str
    international_format_number: str
    international_formatted: str
    national_format_number: str
    country_code: str
    country_name: str
    country_prefix: str
    current_carrier: Carrier
    original_carrier: Carrier
    valid_number: str
    reachable: str
    ported: str
    roaming: str
    gsm_code: Optional[str]
    gsm_message: Optional[str]


hlr_schema = marshmallow_dataclass.class_schema(HlrLookup)()


@dataclass
class Mnp:
    country: str
    number: str
    national_format: str
    international_formatted: str
    network: str
    mccmnc: str
    isPorted: bool
    network_type: str


@dataclass
class MnpResponse:
    code: int
    mnp: Mnp
    price: float
    success: bool


mnp_schema = marshmallow_dataclass.class_schema(MnpResponse)()


@dataclass
class PhoneNumberFormat:
    success: bool
    national: str
    international: str
    international_formatted: str
    country_name: str
    country_code: str
    country_iso: str
    carrier: str
    network_type: str


format_schema = marshmallow_dataclass.class_schema(PhoneNumberFormat)()


@dataclass
class RcsCapabilities(PhoneNumberFormat):
    rcs_capabilities: List[str]


rcs_schema = marshmallow_dataclass.class_schema(RcsCapabilities)()


class LookupResource(Resource):
    def cnam(self, numbers: str | list) -> List[CnamLookup]:
        return self.__get(Endpoint.LOOKUP_CNAM, cnam_schema, numbers)

    def format(self, numbers: str | list) -> List[PhoneNumberFormat]:
        return self.__get(Endpoint.LOOKUP_FORMAT, format_schema, numbers)

    def hlr(self, numbers: str | list) -> List[HlrLookup]:
        return self.__get(Endpoint.LOOKUP_HLR, hlr_schema, numbers)

    def mnp(self, numbers: str | list) -> List[MnpResponse]:
        return self.__get(Endpoint.LOOKUP_MNP, mnp_schema, numbers)

    def rcs(self, numbers: str | list) -> List[RcsCapabilities]:
        return self.__get(Endpoint.LOOKUP_RCS, rcs_schema, numbers)

    def __get(self, endpoint: Endpoint, schema: Schema, numbers: str | list) -> list:
        if isinstance(numbers, str):
            numbers = numbers.split(',')

        numbers = list(filter(str, numbers))
        numbers = list(dict.fromkeys(numbers))

        with self._api.client() as client:
            params = {'number': ','.join(numbers)}
            res = schema.loads(client.get(endpoint.value, params=params).text, many=len(numbers) > 1)
            return res if isinstance(res, list) else [res]
