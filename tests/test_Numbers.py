import uuid

from seven_api.resources.NumbersResource import NumbersResource, AvailableParams, PaymentInterval
from tests.BaseTest import BaseTest


class TestNumbers(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = NumbersResource(self.client)

    def test_numbers_active(self) -> None:
        res = self.resource.active()
        active_numbers = res.activeNumbers
        self.assertTrue(len(active_numbers) > 0)

        for active in active_numbers:
            self.assertTrue(len(active.country) > 0)
            self.assertTrue(len(active.created) > 0)
            if active.expires is not None:
                self.assertTrue(len(active.expires) > 0)
            self.assertTrue(len(active.number) > 0)

            billing = active.billing
            self.assertIn(billing.payment_interval, PaymentInterval.values())

            fees = billing.fees
            self.assertGreaterEqual(fees.basic_charge, 0.0)
            self.assertGreaterEqual(fees.setup, 0.0)
            self.assertGreaterEqual(fees.sms_mo, 0.0)
            self.assertGreaterEqual(fees.voice_mo, 0.0)

            for mail in active.forward_sms_mo.email.address:
                self.assertTrue(len(mail) > 0)

            for number in active.forward_sms_mo.sms.number:
                self.assertTrue(len(number) > 0)

    def test_numbers_available(self) -> None:
        params = AvailableParams(country="DE", features_a2p_sms=True)
        res = self.resource.available(params)

        for offer in res.availableNumbers:
            self.assertEqual(params.country, offer.country)
            self.assertTrue(offer.features.a2p_sms)

    def test_numbers_delete(self) -> None:  # TODO: fix test
        params = AvailableParams()
        params.country = "DE"
        params.features_a2p_sms = True
        res_available = self.resource.available(params)
        available_number = res_available.availableNumbers[0]
        self.assertEqual(params.country, available_number.country)

        number = available_number.number
        print(f'number: {number}\n')

        res_order = self.resource.order(number, PaymentInterval.Monthly)
        print(res_order)
        self.assertIsNone(res_order.error)
        self.assertTrue(res_order.success)

        res = self.resource.delete(number, True)
        self.assertTrue(res.success)

    def test_numbers_update(self) -> None:
        current = self.resource.active().activeNumbers[0]
        updated = self.resource.update(current.number, {
            # 'email_forward': ["joe@seven.dev", "john@seven.dev"],
            'friendly_name': '{}'.format(str(uuid.uuid4())),
            # 'sms_forward': ['49176123456789', '491716992343'],
        })

        self.assertNotEqual(current.friendly_name, updated.friendly_name)
