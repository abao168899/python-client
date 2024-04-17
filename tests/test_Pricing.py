from seven_api.resources.PricingResource import PricingResource, PricingResponse, CountryNetwork, CountryPricing
from tests.BaseTest import BaseTest


class TestPricing(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = PricingResource(self.client)

    def test_pricing_get__global(self) -> None:
        res = self.resource.get()
        self.__assert_response(res)

        for country in res.countries:
            self.__assert_country(country)

    def test_pricing_get__country_code(self) -> None:
        country_code = 'DE'
        res = self.resource.get(country_code)
        self.__assert_response(res)

        self.assertEqual(len(res.countries), 1)
        country = res.countries[0]
        self.__assert_country(country)
        self.assertEqual(country.countryCode, country_code)

    def __assert_country(self, country: CountryPricing):
        for network in country.networks:
            self.__assert_network(network)

    def __assert_network(self, network: CountryNetwork):
        self.assertIsInstance(network.mcc, str)

        if network.mncs is not None:
            for mnc in network.mncs:
                self.assertTrue(len(mnc) > 0)

        if network.networkName is not None:
            self.assertTrue(len(network.networkName) > 0)
        self.assertGreaterEqual(network.price, 0.0)

        for feature in network.features:
            self.assertTrue(len(feature) > 0)

        if network.comment is not None:
            self.assertTrue(len(network.comment) > 0)

    def __assert_response(self, res: PricingResponse):
        self.assertEqual(res.countCountries, len(res.countries))

        networks = 0
        for country in res.countries:
            networks += len(country.networks)

        self.assertEqual(res.countNetworks, networks)
