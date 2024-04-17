from dataclasses import dataclass
from typing import Optional, List

import marshmallow_dataclass

from seven_api.classes.ExtendedEnum import ExtendedEnum
from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource


@dataclass
class Fees:
    basic_charge: float
    setup: float
    sms_mo: float
    voice_mo: float


@dataclass
class Billing:
    fees: Fees
    payment_interval: str


@dataclass
class Features:
    a2p_sms: bool
    sms: bool
    voice: bool


@dataclass
class ForwardInboundSmsToSms:
    enabled: bool
    number: List[str]


@dataclass
class ForwardInboundSmsToMail:
    address: List[str]
    enabled: bool


@dataclass
class ForwardInboundSms:
    email: ForwardInboundSmsToMail
    sms: ForwardInboundSmsToSms


@dataclass
class PhoneNumber:
    billing: Billing
    country: str
    created: str
    expires: Optional[str]
    features: Features
    forward_sms_mo: ForwardInboundSms
    friendly_name: str
    number: str


phone_schema = marshmallow_dataclass.class_schema(PhoneNumber)()


@dataclass
class ActivePhoneNumbers:
    activeNumbers: List[PhoneNumber]


active_schema = marshmallow_dataclass.class_schema(ActivePhoneNumbers)()


@dataclass
class DeleteNumberResponse:
    success: bool


delete_schema = marshmallow_dataclass.class_schema(DeleteNumberResponse)()


@dataclass
class PhoneNumberOfferFeesAmounts:
    basic_charge: float
    setup: float


@dataclass
class PhoneNumberOfferFees:
    annually: PhoneNumberOfferFeesAmounts
    monthly: PhoneNumberOfferFeesAmounts
    sms_mo: float
    voice_mo: float


@dataclass
class PhoneNumberOffer:
    country: str
    features: Features
    fees: PhoneNumberOfferFees
    number: str
    number_parsed: str


@dataclass
class PhoneNumberOffers:
    availableNumbers: List[PhoneNumberOffer]


offers_schema = marshmallow_dataclass.class_schema(PhoneNumberOffers)()

@dataclass
class OrderPhoneNumberResponse:
    error: Optional[str]
    success: bool


order_schema = marshmallow_dataclass.class_schema(OrderPhoneNumberResponse)()

class PaymentInterval(ExtendedEnum):
    Annually = 'annually'
    Monthly = 'monthly'


class AvailableParams(ToQueryString):
    def __init__(self, country: str = "", features_a2p_sms: bool = False, features_sms: bool = False,
                 features_voice: bool = False):
        self.country = country
        self.features_a2p_sms = features_a2p_sms
        self.features_sms = features_sms
        self.features_voice = features_voice

    def __iter__(self):
        yield 'country', self.country
        yield 'features_a2p_sms', str(self.features_a2p_sms).lower()
        yield 'features_sms', str(self.features_sms).lower()
        yield 'features_voice', str(self.features_voice).lower()


class NumbersResource(Resource):
    def active(self) -> ActivePhoneNumbers:
        with self._api.client() as client:
            return active_schema.loads(client.get(Endpoint.NUMBERS_ACTIVE.value).text)

    def available(self, params: AvailableParams = None) -> PhoneNumberOffers:
        if params is None:
            params = AvailableParams()

        with self._api.client() as client:
            return offers_schema.loads(client.get(Endpoint.NUMBERS_AVAILABLE.value, params=params.as_dict()).text)

    def delete(self, number: str, delete_immediately: bool = False) -> DeleteNumberResponse:
        params = {}
        if delete_immediately:
            params.update({'delete_immediately': 'true'})
        with self._api.client() as client:
            return delete_schema.loads(client.delete(f'{Endpoint.NUMBERS_ACTIVE.value}/{number}', params=params).text)

    def get(self, number: str) -> PhoneNumber:
        with self._api.client() as client:
            return phone_schema.loads(client.get(f'{Endpoint.NUMBERS_ACTIVE.value}/{number}').text)

    def order(self, number: str, interval: PaymentInterval = PaymentInterval.Annually) -> OrderPhoneNumberResponse:
        params = {'number': number, 'payment_interval': interval.value}
        print(params)
        with self._api.client() as client:
            return order_schema.loads(client.post(Endpoint.NUMBERS_ORDER, data=params).text)

    def update(self, number: str, params: dict) -> PhoneNumber:
        with self._api.client() as client:
            return phone_schema.loads(client.patch(f'{Endpoint.NUMBERS_ACTIVE.value}/{number}', data=params).text)
