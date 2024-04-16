from seven_api.resources.PricingResource import PricingResource
from tests.BaseTest import BaseTest


class TestPricing(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = PricingResource(self.client)

    def test_pricing_get__global(self) -> None:
        res = self.resource.get()
        self.__assert_response(res)

        for country in res['countries']:
            self.__assert_country(country)

    def test_pricing_get__country_code(self) -> None:
        country_code = 'DE'
        res = self.resource.get(country_code)
        self.__assert_response(res)

        self.assertEqual(len(res['countries']), 1)
        for country in res['countries']:
            self.__assert_country(country)
            self.assertEqual(country['countryCode'], country_code)

    def __assert_country(self, country: dict):
        self.assertIsInstance(country['countryCode'], str)
        self.assertIsInstance(country['countryName'], str)
        self.assertIsInstance(country['countryPrefix'], str)
        self.assertIsInstance(country['networks'], list)

        for network in country['networks']:
            self.__assert_network(network)

    def __assert_network(self, network: dict):
        self.assertIsInstance(network['mcc'], str)

        mncs = network['mncs']
        self.assertTrue(mncs is None or type(mncs) is list)
        if mncs is not None:
            mnc = BaseTest.first_list_item_fallback(mncs)
            if mnc:
                self.assertIsInstance(mnc, str)

        network_name = network['networkName']
        self.assertTrue(network_name is None or type(network_name) is str)
        self.assertIsInstance(network['price'], float)
        self.assertIsInstance(network['features'], list)
        comment = network['comment']
        self.assertTrue(comment is None or type(comment) is str)

    def __assert_response(self, res: dict):
        self.assertIsInstance(res['countCountries'], int)
        self.assertIsInstance(res['countNetworks'], int)
        self.assertIsInstance(res['countries'], list)
