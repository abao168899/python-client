from seven_api.classes.ExtendedEnum import ExtendedEnum
from seven_api.classes.Endpoint import Endpoint
from seven_api.classes.ToQueryString import ToQueryString
from seven_api.resources.Resource import Resource


class PaymentInterval(ExtendedEnum):
    Annually = 'annually'
    Monthly = 'monthly'


class AvailableParams(ToQueryString):
    country: str = ""
    features_a2p_sms: bool = False
    features_sms: bool = False
    features_voice: bool = False

    def __iter__(self):
        yield 'country', self.country
        yield 'features_a2p_sms', str(self.features_a2p_sms).lower()
        yield 'features_sms', str(self.features_sms).lower()
        yield 'features_voice', str(self.features_voice).lower()


class NumbersResource(Resource):
    def active(self) -> dict:
        return self._client.get(Endpoint.NUMBERS_ACTIVE)

    def available(self, params: AvailableParams = None) -> dict:
        if params is None:
            params = AvailableParams()

        return self._client.get(Endpoint.NUMBERS_AVAILABLE, params.as_dict())

    def delete(self, number: str, delete_immediately: bool = False) -> dict:
        path = f'{Endpoint.NUMBERS_ACTIVE.value}/{number}'
        if delete_immediately:
            path += f'?delete_immediately={str(delete_immediately).lower()}'
        return self._client.delete(path)

    def get(self, number: str) -> dict:
        return self._client.get(f'{Endpoint.NUMBERS_ACTIVE.value}/{number}')

    def order(self, number: str, payment_interval: PaymentInterval = PaymentInterval.Annually) -> dict:
        params = {'number': number, 'payment_interval': payment_interval.value}
        print(params)
        return self._client.post(Endpoint.NUMBERS_ORDER, params)

    def update(self, number: str, params: dict) -> dict:
        return self._client.patch(f'{Endpoint.NUMBERS_ACTIVE.value}/{number}', params)
