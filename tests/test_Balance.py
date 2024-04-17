from seven_api.resources.BalanceResource import BalanceResource
from tests.BaseTest import BaseTest


class TestBalance(BaseTest):
    def test_balance(self) -> None:
        res = BalanceResource(self.client).retrieve()

        self.assertEqual('EUR', res.currency)
