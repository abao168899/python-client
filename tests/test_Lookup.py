from seven_api.resources.LookupResource import LookupResource
from tests.BaseTest import BaseTest


class TestLookup(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = LookupResource(self.client)

    def test_lookup_cnam(self) -> None:
        for lookup in self.resource.cnam('+491716992343'):
            self.assertIsInstance(lookup, dict)
            self.assertIsInstance(lookup['success'], str)
            self.assertIsInstance(lookup['code'], str)
            self.assertIsInstance(lookup['number'], str)
            self.assertIsInstance(lookup['name'], str)

    def test_lookup_format(self) -> None:
        for lookup in self.resource.format('+491716992343'):
            self.assert_format(lookup)

    def test_lookup_hlr(self) -> None:
        def is_valid_carrier(carrier: dict):
            valid = isinstance(carrier['network_code'], str)
            valid = isinstance(carrier['name'], str) if valid else False
            valid = isinstance(carrier['country'], str) if valid else False
            valid = isinstance(carrier['network_type'], str) if valid else False

            return valid

        for lookup in self.resource.hlr('+491716992343'):
            self.assertIsInstance(lookup, dict)
            self.assertIsInstance(lookup['status'], bool)
            self.assertIsInstance(lookup['status_message'], str)
            self.assertIsInstance(lookup['lookup_outcome'], bool)
            self.assertIsInstance(lookup['lookup_outcome_message'], str)
            self.assertIsInstance(lookup['international_format_number'], str)
            self.assertIsInstance(lookup['international_formatted'], str)
            self.assertIsInstance(lookup['national_format_number'], str)
            self.assertIsInstance(lookup['country_code'], str)
            self.assertIsInstance(lookup['country_name'], str)
            self.assertIsInstance(lookup['country_prefix'], str)
            self.assertIsInstance(lookup['current_carrier'], dict)
            self.assertIsInstance(lookup['original_carrier'], dict)
            self.assertIsInstance(lookup['valid_number'], str)
            self.assertIsInstance(lookup['reachable'], str)
            self.assertIsInstance(lookup['ported'], str)
            self.assertIsInstance(lookup['roaming'], str)
            self.assertIsNone(lookup['gsm_code'])
            self.assertIsNone(lookup['gsm_message'])
            self.assertTrue(is_valid_carrier(lookup['current_carrier']))
            self.assertTrue(is_valid_carrier(lookup['original_carrier']))

    def test_lookup_mnp(self) -> None:
        for lookup in self.resource.mnp('+491716992343'):
            self.assertIsInstance(lookup, dict)

            self.assertTrue(lookup['success'])
            self.assertEqual(lookup['code'], 100)
            self.assertIsInstance(lookup['price'], float)
            self.assertIsInstance(lookup['mnp'], dict)

            self.assertIsInstance(lookup['mnp']['country'], str)
            self.assertIsInstance(lookup['mnp']['number'], str)
            self.assertIsInstance(lookup['mnp']['national_format'], str)
            self.assertIsInstance(lookup['mnp']['international_formatted'], str)
            self.assertIsInstance(lookup['mnp']['network'], str)
            self.assertIsInstance(lookup['mnp']['mccmnc'], str)
            self.assertIsInstance(lookup['mnp']['isPorted'], bool)

    def test_lookup_rcs(self) -> None:
        for lookup in self.resource.rcs('+491716992343'):
            self.assertIsInstance(lookup['rcs_capabilities'], list)
            self.assert_format(lookup)

    def assert_format(self, res: dict) -> None:
        self.assertTrue(res['success'])
        self.assertIsInstance(res['national'], str)
        self.assertIsInstance(res['international'], str)
        self.assertIsInstance(res['international_formatted'], str)
        self.assertIsInstance(res['country_name'], str)
        self.assertIsInstance(res['country_code'], str)
        self.assertIsInstance(res['country_iso'], str)
        self.assertIsInstance(res['carrier'], str)
        self.assertIsInstance(res['network_type'], str)
