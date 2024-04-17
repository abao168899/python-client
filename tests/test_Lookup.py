from seven_api.resources.LookupResource import LookupResource, RcsCapabilities, PhoneNumberFormat, Carrier, CnamLookup
from tests.BaseTest import BaseTest


class TestLookup(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = LookupResource(self.client)

    def __assertCnam(self, cnam: CnamLookup):
        self.assertTrue(len(cnam.code) > 0)
        self.assertTrue(len(cnam.name) > 0)
        self.assertTrue(len(cnam.number) > 0)
        self.assertIn(cnam.success, ['true', 'false'])

    def test_lookup_cnam(self) -> None:
        res = self.resource.cnam('+491716992343')
        self.assertEqual(1, len(res))

        for lookup in res:
            self.__assertCnam(lookup)

    def test_lookup_cnam__multi(self) -> None:
        numbers = ['491716992343', '491799999999']
        res = self.resource.cnam(numbers)
        self.assertEqual(len(numbers), len(res))

        for lookup in res:
            self.assertIn(lookup.number, numbers)
            self.__assertCnam(lookup)

    def test_lookup_format(self) -> None:
        res = self.resource.format('+491716992343')
        self.assertEqual(1, len(res))

        for lookup in res:
            self.__assertFormat(lookup)

    def test_lookup_format__multi(self) -> None:
        numbers = ['+491716992343', '+491799999999']
        res = self.resource.format(numbers)
        self.assertEqual(len(numbers), len(res))

        for lookup in res:
            self.assertIn(lookup.international, numbers)
            self.__assertFormat(lookup)

    def test_lookup_hlr(self) -> None:
        def is_valid_carrier(carrier: Carrier):
            valid = isinstance(carrier.network_code, str)
            valid = isinstance(carrier.name, str) if valid else False
            valid = isinstance(carrier.country, str) if valid else False
            valid = isinstance(carrier.network_type, str) if valid else False

            return valid

        for hlr in self.resource.hlr('+491716992343'):
            self.assertIsInstance(hlr.status, bool)
            self.assertIsInstance(hlr.status_message, str)
            self.assertIsInstance(hlr.lookup_outcome, bool)
            self.assertIsInstance(hlr.lookup_outcome_message, str)
            self.assertIsInstance(hlr.international_format_number, str)
            self.assertIsInstance(hlr.international_formatted, str)
            self.assertIsInstance(hlr.national_format_number, str)
            self.assertIsInstance(hlr.country_code, str)
            self.assertIsInstance(hlr.country_name, str)
            self.assertIsInstance(hlr.country_prefix, str)
            self.assertIsInstance(hlr.valid_number, str)
            self.assertIsInstance(hlr.reachable, str)
            self.assertIsInstance(hlr.ported, str)
            self.assertIsInstance(hlr.roaming, str)
            self.assertIsNone(hlr.gsm_code)
            self.assertIsNone(hlr.gsm_message)
            self.assertTrue(is_valid_carrier(hlr.current_carrier))
            self.assertTrue(is_valid_carrier(hlr.original_carrier))

    def test_lookup_mnp(self) -> None:
        for mnp in self.resource.mnp('+491716992343'):
            self.assertTrue(mnp.success)
            self.assertEqual(mnp.code, 100)
            self.assertGreaterEqual(mnp.price, 0.0)

            self.assertTrue(len(mnp.mnp.country) > 0)
            self.assertTrue(len(mnp.mnp.number) > 0)
            self.assertTrue(len(mnp.mnp.national_format) > 0)
            self.assertTrue(len(mnp.mnp.international_formatted) > 0)
            self.assertTrue(len(mnp.mnp.network) > 0)
            self.assertTrue(len(mnp.mnp.mccmnc) > 0)
            self.assertIsInstance(mnp.mnp.isPorted, bool)

    def test_lookup_rcs(self) -> None:
        lookup: RcsCapabilities
        for lookup in self.resource.rcs('+491716992343'):
            self.assertIsInstance(lookup.rcs_capabilities, list)
            self.__assertFormat(lookup)

    def __assertFormat(self, res: PhoneNumberFormat) -> None:
        self.assertTrue(res.success)
        self.assertTrue(len(res.national) > 0)
        self.assertTrue(len(res.international) > 0)
        self.assertTrue(len(res.international_formatted) > 0)
        self.assertTrue(len(res.country_name) > 0)
        self.assertTrue(len(res.country_code) > 0)
        self.assertTrue(len(res.country_iso) > 0)
        self.assertTrue(len(res.carrier) > 0)
        self.assertTrue(len(res.network_type) > 0)
